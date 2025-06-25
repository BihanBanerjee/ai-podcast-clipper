# AI Podcast Clipper

An intelligent podcast processing platform that automatically generates short clips from podcast videos using AI-powered transcription, active speaker detection, and content analysis.

## 🎯 Features

- **AI-Powered Clip Generation**: Automatically identifies and extracts engaging Q&A segments and stories from podcast content
- **Active Speaker Detection**: Uses computer vision to detect and track speakers, creating vertical videos optimized for social media
- **Automatic Transcription**: Leverages WhisperX for accurate speech-to-text conversion with word-level timestamps
- **Smart Subtitles**: Generates and burns in subtitles with custom styling for better engagement
- **Credit-Based System**: Flexible pricing model with Stripe integration
- **S3 Storage**: Scalable cloud storage for video files and generated clips
- **Modern UI**: Built with Next.js 14, React, and Tailwind CSS using shadcn/ui components

## 🏗️ Architecture

### Backend (Modal + Python)
- **Modal**: Serverless GPU compute for video processing
- **WhisperX**: Advanced speech recognition with alignment
- **OpenCV + ffmpeg**: Video processing and manipulation
- **Google Gemini**: AI-powered content analysis for clip identification
- **Active Speaker Detection**: Computer vision model for speaker tracking

### Frontend (Next.js 14 + T3 Stack)
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Prisma**: Database ORM with PostgreSQL
- **NextAuth.js**: Authentication system
- **Tailwind CSS**: Utility-first styling
- **shadcn/ui**: Modern UI components
- **tRPC**: Type-safe API layer

### Infrastructure
- **AWS S3**: File storage and delivery
- **PostgreSQL**: Primary database
- **Stripe**: Payment processing
- **Inngest**: Background job processing

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Python 3.12+
- PostgreSQL database
- AWS account with S3 bucket
- Stripe account
- Modal account
- Google AI Studio account (for Gemini API)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-podcast-clipper-backend
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Modal secrets**
   ```bash
   modal secret create ai-podcast-clipper-secret \
     GEMINI_API_KEY=your_gemini_api_key \
     AUTH_TOKEN=your_auth_token
   ```

4. **Deploy to Modal**
   ```bash
   modal deploy main.py
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ai-podcast-clipper-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

3. **Set up environment variables**
   Create a `.env` file in the frontend directory:
   ```env
   # Database
   DATABASE_URL="postgresql://username:password@localhost:5432/podcast_clipper"
   
   # NextAuth
   AUTH_SECRET="your-secret-key"
   
   # AWS S3
   AWS_ACCESS_KEY_ID="your-access-key"
   AWS_SECRET_ACCESS_KEY="your-secret-key"
   AWS_REGION="us-east-1"
   S3_BUCKET_NAME="your-bucket-name"
   
   # Modal Processing Endpoint
   PROCESS_VIDEO_ENDPOINT="https://your-modal-app.modal.run/process_video"
   PROCESS_VIDEO_ENDPOINT_AUTH="your-auth-token"
   
   # Stripe
   STRIPE_SECRET_KEY="sk_test_..."
   STRIPE_WEBHOOK_SECRET="whsec_..."
   STRIPE_SMALL_CREDIT_PACK="price_..."
   STRIPE_MEDIUM_CREDIT_PACK="price_..."
   STRIPE_LARGE_CREDIT_PACK="price_..."
   NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY="pk_test_..."
   
   # App
   BASE_URL="http://localhost:3000"
   ```

4. **Set up the database**
   ```bash
   npx prisma generate
   npx prisma db push
   ```

5. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

Open [http://localhost:3000](http://localhost:3000) to view the application.

## 📊 Database Schema

The application uses PostgreSQL with the following main entities:

- **User**: User accounts with credits and Stripe integration
- **UploadedFile**: Podcast files with processing status
- **Clip**: Generated clips linked to uploaded files
- **Account/Session**: NextAuth.js authentication tables

## 🔄 Processing Pipeline

1. **Upload**: User uploads MP4 file to S3 via signed URL
2. **Queue**: Background job queued using Inngest
3. **Transcription**: WhisperX processes audio for word-level timestamps
4. **Content Analysis**: Gemini AI identifies interesting Q&A segments
5. **Video Processing**: Active speaker detection and vertical video creation
6. **Subtitle Generation**: Automatic subtitle creation and burning
7. **Storage**: Processed clips uploaded to S3
8. **Database Update**: Clip records created and user credits deducted

## 💳 Credit System

- 1 credit = 1 minute of podcast processing
- Approximately 1 clip generated per 5 minutes of content
- Three pricing tiers:
  - Small Pack: 50 credits for $9.99
  - Medium Pack: 150 credits for $24.99 (17% savings)
  - Large Pack: 500 credits for $69.99 (30% savings)

## 🎨 UI Components

Built with modern, accessible components:

- **File Upload**: Drag-and-drop interface with progress tracking
- **Processing Status**: Real-time status updates with refresh capability
- **Clip Gallery**: Grid view of generated clips with download functionality
- **Credit Management**: Display current credits with purchase options
- **Authentication**: Secure login/signup with form validation

## 🔧 API Endpoints

### Backend (Modal)
- `POST /process_video`: Main video processing endpoint

### Frontend (Next.js API Routes)
- `POST /api/auth/[...nextauth]`: Authentication endpoints
- `POST /api/webhooks/stripe`: Stripe webhook handler
- `GET/POST /api/inngest`: Background job processing

## 🛠️ Development

### Backend Development
```bash
# Run local development
modal run main.py

# View logs
modal logs ai-podcast-clipper

# Update deployment
modal deploy main.py
```

### Frontend Development
```bash
# Run development server
npm run dev

# Run database migrations
npx prisma db push

# Generate Prisma client
npx prisma generate

# View database
npx prisma studio
```

## 🚀 Deployment

### Backend
The backend is automatically deployed to Modal. Update the deployment with:
```bash
modal deploy main.py
```

### Frontend
Deploy to Vercel or your preferred platform:
```bash
# Build the application
npm run build

# Start production server
npm start
```

## 📝 Environment Variables

Refer to `src/env.js` for the complete list of required environment variables and their validation schemas.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please open an issue in the GitHub repository or contact the development team.

## 🙏 Acknowledgments

- WhisperX for advanced speech recognition
- Modal for serverless GPU compute
- T3 Stack for the excellent Next.js boilerplate
- shadcn/ui for beautiful UI components