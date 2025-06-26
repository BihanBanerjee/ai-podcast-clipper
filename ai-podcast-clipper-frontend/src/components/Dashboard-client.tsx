"use client";

import Dropzone, { type DropzoneState } from "shadcn-dropzone";
import type { Clip } from "@prisma/client";
import Link from "next/link";
import { Button } from "./ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "./ui/card";
import { Loader2, UploadCloud, Youtube } from "lucide-react";
import { useState } from "react";
import { generateUploadUrl } from "~/actions/s3";
import { toast } from "sonner";
import { processVideo, processYouTubeVideo } from "~/actions/generation";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./ui/table";
import { Badge } from "./ui/badge";
import { useRouter } from "next/navigation";
import { ClipDisplay } from "./Clip-display";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import { Label } from "./ui/label";
import { Input } from "./ui/input";

export function DashboardClient({
  uploadedFiles,
  clips,
}: {
  uploadedFiles: {
    id: string;
    s3Key: string;
    filename: string;
    status: string;
    clipsCount: number;
    createdAt: Date;
  }[];
  clips: Clip[];
}) {
  const [files, setFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [processingYoutube, setProcessingYoutube] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedMode, setSelectedMode] = useState("question");
  const [uploadMethod, setUploadMethod] = useState<"file" | "youtube">("file");
  const router = useRouter();

  // Define the clip modes
  const clipModes = [
    { value: "question", label: "Question & Answer", description: "Q&A segments and discussions" },
    { value: "story", label: "Stories & Anecdotes", description: "Personal stories and experiences" },
    { value: "quote", label: "Memorable Quotes", description: "Quotable moments and one-liners" },
    { value: "controversial", label: "Hot Takes", description: "Controversial opinions and debates" },
    { value: "educational", label: "Tips & Tutorials", description: "Educational content and advice" },
    { value: "emotional", label: "Emotional Moments", description: "High emotion and genuine reactions" },
    { value: "laughter", label: "Laughter Mode", description: "Funny moments and comedic segments" },
    { value: "insight", label: "Key Insights", description: "Important realizations and insights" },
    { value: "contradiction", label: "Contradiction Mode", description: "Disagreements and opposing views" },
    { value: "vulnerability", label: "Vulnerability Mode", description: "Personal confessions and authentic sharing" },
    { value: "actionable", label: "Actionable Mode", description: "Specific advice listeners can implement" },
    { value: "energy", label: "Energy Spike Mode", description: "High-energy and passionate moments" }
  ];

  const handleRefresh = async () => {
    setRefreshing(true);
    router.refresh();
    setTimeout(() => setRefreshing(false), 600);
  };

  const handleDrop = (acceptedFiles: File[]) => {
    setFiles(acceptedFiles);
  };

  const handleFileUpload = async () => {
    if (files.length === 0) return;

    const file = files[0]!;
    setUploading(true);

    try {
      const { success, signedUrl, uploadedFileId } = await generateUploadUrl({
        filename: file.name,
        contentType: file.type,
      });

      if (!success) throw new Error("Failed to get upload URL");

      const uploadResponse = await fetch(signedUrl, {
        method: "PUT",
        body: file,
        headers: {
          "Content-Type": file.type,
        },
      });

      if (!uploadResponse.ok)
        throw new Error(`Upload failed with status: ${uploadResponse.status}`);

      // Pass the selected mode to processVideo
      await processVideo(uploadedFileId, selectedMode);

      setFiles([]);

      const selectedModeLabel = clipModes.find(m => m.value === selectedMode)?.label ?? selectedMode;
      toast.success("Video uploaded successfully", {
        description: `Processing with ${selectedModeLabel} mode. Check the status below.`,
        duration: 5000,
      });
    } catch (error) {
      toast.error("Upload failed", {
        description: "There was a problem uploading your video. Please try again.",
      });
    } finally {
      setUploading(false);
    }
  };

  const handleYouTubeSubmit = async () => {
    if (!youtubeUrl.trim()) {
      toast.error("Please enter a valid YouTube URL");
      return;
    }

    setProcessingYoutube(true);

    try {
      await processYouTubeVideo(youtubeUrl, selectedMode);
      
      const selectedModeLabel = clipModes.find(m => m.value === selectedMode)?.label ?? selectedMode;
      toast.success("YouTube video processing started", {
        description: `Processing with ${selectedModeLabel} mode. This may take a few minutes.`,
        duration: 5000,
      });

      setYoutubeUrl("");
    } catch (error) {
      toast.error("Processing failed", {
        description: error instanceof Error ? error.message : "Failed to process YouTube video. Please try again.",
      });
    } finally {
      setProcessingYoutube(false);
    }
  };

  return (
    <div className="mx-auto flex max-w-5xl flex-col space-y-6 px-4 py-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Podcast Clipper
          </h1>
          <p className="text-muted-foreground">
            Upload your podcast or provide a YouTube link to get AI-generated clips instantly
          </p>
        </div>
        <Link href="/dashboard/billing">
          <Button>Buy Credits</Button>
        </Link>
      </div>

      <Tabs defaultValue="upload">
        <TabsList>
          <TabsTrigger value="upload">Upload</TabsTrigger>
          <TabsTrigger value="my-clips">My Clips</TabsTrigger>
        </TabsList>

        <TabsContent value="upload">
          <Card>
            <CardHeader>
              <CardTitle>Upload Podcast</CardTitle>
              <CardDescription>
                Upload your audio/video file or provide a YouTube link to generate clips
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Upload Method Selection */}
              <div className="space-y-3">
                <Label>Choose upload method</Label>
                <div className="flex gap-4">
                  <Button
                    type="button"
                    variant={uploadMethod === "file" ? "default" : "outline"}
                    onClick={() => setUploadMethod("file")}
                    className="flex items-center gap-2"
                  >
                    <UploadCloud className="h-4 w-4" />
                    Upload File
                  </Button>
                  <Button
                    type="button"
                    variant={uploadMethod === "youtube" ? "default" : "outline"}
                    onClick={() => setUploadMethod("youtube")}
                    className="flex items-center gap-2"
                  >
                    <Youtube className="h-4 w-4" />
                    YouTube Link
                  </Button>
                </div>
              </div>

              {/* File Upload */}
              {uploadMethod === "file" && (
                <Dropzone
                  onDrop={handleDrop}
                  accept={{ "video/mp4": [".mp4"] }}
                  maxSize={500 * 1024 * 1024}
                  disabled={uploading}
                  maxFiles={1}
                >
                  {(dropzone: DropzoneState) => (
                    <>
                      <div className="flex flex-col items-center justify-center space-y-4 rounded-lg p-10 text-center">
                        <UploadCloud className="text-muted-foreground h-12 w-12" />
                        <p className="font-medium">Drag and drop your file</p>
                        <p className="text-muted-foreground text-sm">
                          or click to browse (MP4 up to 500MB)
                        </p>
                        <Button
                          className="cursor-pointer"
                          variant="default"
                          size="sm"
                          disabled={uploading}
                        >
                          Select File
                        </Button>
                      </div>
                    </>
                  )}
                </Dropzone>
              )}

              {/* YouTube URL Input */}
              {uploadMethod === "youtube" && (
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="youtube-url">YouTube URL</Label>
                    <Input
                      id="youtube-url"
                      type="url"
                      placeholder="https://www.youtube.com/watch?v=..."
                      value={youtubeUrl}
                      onChange={(e) => setYoutubeUrl(e.target.value)}
                      disabled={processingYoutube}
                    />
                  </div>
                  <div className="text-sm text-muted-foreground">
                    <p>Supported formats: YouTube video URLs (youtube.com/watch or youtu.be)</p>
                  </div>
                </div>
              )}

              {/* Mode Selection */}
              <div className="space-y-2">
                <Label htmlFor="clip-mode">Clip Generation Mode</Label>
                <Select value={selectedMode} onValueChange={setSelectedMode}>
                  <SelectTrigger className="w-full h-12">
                    <SelectValue placeholder="Select clipping mode" />
                  </SelectTrigger>
                  <SelectContent className="max-h-[400px]">
                    {clipModes.map((mode) => (
                      <SelectItem 
                        key={mode.value} 
                        value={mode.value}
                        className="py-3 px-3"
                      >
                        <div className="flex flex-col space-y-1">
                          <span className="font-medium text-sm">{mode.label}</span>
                          <span className="text-xs text-muted-foreground leading-relaxed">
                            {mode.description}
                          </span>
                        </div>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Action Button */}
              <div className="flex items-start justify-between">
                <div>
                  {uploadMethod === "file" && files.length > 0 && (
                    <div className="space-y-1 text-sm">
                      <p className="font-medium">Selected file:</p>
                      {files.map((file) => (
                        <p key={file.name} className="text-muted-foreground">
                          {file.name}
                        </p>
                      ))}
                    </div>
                  )}
                  {uploadMethod === "youtube" && youtubeUrl && (
                    <div className="space-y-1 text-sm">
                      <p className="font-medium">YouTube URL:</p>
                      <p className="text-muted-foreground truncate max-w-md">
                        {youtubeUrl}
                      </p>
                    </div>
                  )}
                </div>
                
                {uploadMethod === "file" ? (
                  <Button
                    disabled={files.length === 0 || uploading}
                    onClick={handleFileUpload}
                  >
                    {uploading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Uploading...
                      </>
                    ) : (
                      "Upload and Generate Clips"
                    )}
                  </Button>
                ) : (
                  <Button
                    disabled={!youtubeUrl.trim() || processingYoutube}
                    onClick={handleYouTubeSubmit}
                  >
                    {processingYoutube ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Processing...
                      </>
                    ) : (
                      "Process YouTube Video"
                    )}
                  </Button>
                )}
              </div>

              {uploadedFiles.length > 0 && (
                <div className="pt-6">
                  <div className="mb-2 flex items-center justify-between">
                    <h3 className="text-md mb-2 font-medium">Queue status</h3>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handleRefresh}
                      disabled={refreshing}
                    >
                      {refreshing && (
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      )}
                      Refresh
                    </Button>
                  </div>
                  <div className="max-h-[300px] overflow-auto rounded-md border">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>File</TableHead>
                          <TableHead>Uploaded</TableHead>
                          <TableHead>Status</TableHead>
                          <TableHead>Clips created</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {uploadedFiles.map((item) => (
                          <TableRow key={item.id}>
                            <TableCell className="max-w-xs truncate font-medium">
                              {item.filename}
                            </TableCell>
                            <TableCell className="text-muted-foreground text-sm">
                              {new Date(item.createdAt).toLocaleDateString()}
                            </TableCell>
                            <TableCell>
                              {item.status === "queued" && (
                                <Badge variant="outline">Queued</Badge>
                              )}
                              {item.status === "processing" && (
                                <Badge variant="outline">Processing</Badge>
                              )}
                              {item.status === "processed" && (
                                <Badge variant="outline">Processed</Badge>
                              )}
                              {item.status === "no credits" && (
                                <Badge variant="destructive">No credits</Badge>
                              )}
                              {item.status === "failed" && (
                                <Badge variant="destructive">Failed</Badge>
                              )}
                            </TableCell>
                            <TableCell>
                              {item.clipsCount > 0 ? (
                                <span>
                                  {item.clipsCount} clip
                                  {item.clipsCount !== 1 ? "s" : ""}
                                </span>
                              ) : (
                                <span className="text-muted-foreground">
                                  No clips yet
                                </span>
                              )}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="my-clips">
          <Card>
            <CardHeader>
              <CardTitle>My Clips</CardTitle>
              <CardDescription>
                View and manage your generated clips here. Processing may take a
                few minutes.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ClipDisplay clips={clips} />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}