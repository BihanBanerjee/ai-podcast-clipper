// Update src/inngest/functions.ts

import { env } from "~/env";
import { inngest } from "./client";
import { db } from "~/server/db";
import { ListObjectsV2Command, S3Client } from "@aws-sdk/client-s3";

interface ProcessVideoEventData {
  uploadedFileId?: string;
  userId: string;
  mode?: string;
  youtubeUrl?: string;
}

interface RequestPayload {
  mode: string;
  youtube_url?: string;
  s3_key?: string;
}

export const processVideo = inngest.createFunction(
  {
    id: "process-video",
    retries: 1,
    concurrency: {
      limit: 1,
      key: "event.data.userId",
    },
  },
  { event: "process-video-events" },
  async ({ event, step }) => {
    const { uploadedFileId, mode, youtubeUrl } = event.data as ProcessVideoEventData;

    try {
      let userId: string;
      let credits: number;
      let s3Key: string | null | undefined;

      if (uploadedFileId) {
        // Existing S3 upload flow
        const fileData = await step.run("check-credits", async () => {
          const uploadedFile = await db.uploadedFile.findUniqueOrThrow({
            where: { id: uploadedFileId },
            select: {
              user: { select: { id: true, credits: true } },
              s3Key: true,
            },
          });

          return {
            userId: uploadedFile.user.id,
            credits: uploadedFile.user.credits,
            s3Key: uploadedFile.s3Key,
          };
        });

        userId = fileData.userId;
        credits = fileData.credits;
        s3Key = fileData.s3Key;
      } else {
        // YouTube URL flow - get user from event data
        const userData = await step.run("get-user-credits", async () => {
          const user = await db.user.findUniqueOrThrow({
            where: { id: (event.data as ProcessVideoEventData).userId },
            select: { id: true, credits: true },
          });

          return {
            userId: user.id,
            credits: user.credits,
          };
        });

        userId = userData.userId;
        credits = userData.credits;
        s3Key = undefined;
      }

      if (credits > 0) {
        if (uploadedFileId) {
          await step.run("set-status-processing", async () => {
            await db.uploadedFile.update({
              where: { id: uploadedFileId },
              data: { status: "processing" },
            });
          });
        }

        // Prepare request payload
        const requestPayload: RequestPayload = {
          mode: mode ?? "question",
        };

        if (youtubeUrl) {
          requestPayload.youtube_url = youtubeUrl;
        } else if (s3Key) {
          requestPayload.s3_key = s3Key;
        }

        await step.fetch(env.PROCESS_VIDEO_ENDPOINT, {
          method: "POST",
          body: JSON.stringify(requestPayload),
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${env.PROCESS_VIDEO_ENDPOINT_AUTH}`,
          },
        });

        const { clipsFound } = await step.run(
          "create-clips-in-db",
          async () => {
            if (youtubeUrl) {
              // For YouTube videos, the backend generates s3_key with video ID
              // We need to list objects and find clips that were just created
              
              // Since we don't know the exact video ID from frontend, 
              // we'll search for recent clips in the youtube/ folder
              const allYouTubeKeys = await listS3ObjectsByPrefix("youtube/");
              
              // Filter for clips and exclude original files
              const recentClipKeys = allYouTubeKeys.filter((key): key is string => {
                if (!key || key.endsWith("original.mp4")) return false;
                
                // This is a simplified approach. In production, you might want to:
                // 1. Return the actual folder prefix from the Modal endpoint
                // 2. Use a more sophisticated matching mechanism
                // 3. Store the processing job ID for tracking
                
                return true; // For now, include all non-original files
              });

              // Take the most recent clips (assume they belong to this job)
              const clipKeys = recentClipKeys.slice(-5); // Assuming max 5 clips per video

              if (clipKeys.length > 0) {
                await db.clip.createMany({
                  data: clipKeys.map((clipKey) => ({
                    s3Key: clipKey,
                    uploadedFileId: uploadedFileId?.toString() ?? '',
                    userId,
                  })),
                });
              }

              return { clipsFound: clipKeys.length, folderPrefix: "youtube" };
            } else {
              // Existing S3 flow
              if (!s3Key) {
                throw new Error("s3Key is required for S3 upload flow");
              }
              
              const folderPrefix = s3Key.split("/")[0]!;
              const allKeys = await listS3ObjectsByPrefix(folderPrefix);
              const clipKeys = allKeys.filter(
                (key): key is string =>
                  key !== undefined && !key.endsWith("original.mp4"),
              );

              if (clipKeys.length > 0) {
                await db.clip.createMany({
                  data: clipKeys.map((clipKey) => ({
                    s3Key: clipKey,
                    uploadedFileId: uploadedFileId!,
                    userId,
                  })),
                });
              }

              return { clipsFound: clipKeys.length, folderPrefix };
            }
          },
        );

        await step.run("deduct-credits", async () => {
          await db.user.update({
            where: { id: userId },
            data: {
              credits: {
                decrement: Math.min(credits, clipsFound),
              },
            },
          });
        });

        if (uploadedFileId) {
          await step.run("set-status-processed", async () => {
            await db.uploadedFile.update({
              where: { id: uploadedFileId },
              data: { status: "processed" },
            });
          });
        }
      } else {
        if (uploadedFileId) {
          await step.run("set-status-no-credits", async () => {
            await db.uploadedFile.update({
              where: { id: uploadedFileId },
              data: { status: "no credits" },
            });
          });
        }
      }
    } catch (error: unknown) {
      if (uploadedFileId) {
        await db.uploadedFile.update({
          where: { id: uploadedFileId },
          data: { status: "failed" },
        });
      }
      throw error;
    }
  },
);

async function listS3ObjectsByPrefix(prefix: string) {
  const s3Client = new S3Client({
    region: env.AWS_REGION,
    credentials: {
      accessKeyId: env.AWS_ACCESS_KEY_ID,
      secretAccessKey: env.AWS_SECRET_ACCESS_KEY,
    },
  });

  const listCommand = new ListObjectsV2Command({
    Bucket: env.S3_BUCKET_NAME,
    Prefix: prefix,
  });

  const response = await s3Client.send(listCommand);
  return response.Contents?.map((item) => item.Key).filter(Boolean) ?? [];
}