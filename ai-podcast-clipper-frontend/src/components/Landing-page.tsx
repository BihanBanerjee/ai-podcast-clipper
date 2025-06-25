"use client";

import Link from "next/link";
import { Button } from "~/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card";
import { Badge } from "~/components/ui/badge";
import { 
  PlayCircle, 
  Scissors, 
  Upload, 
  Download, 
  Star, 
  Clock, 
  Zap, 
  CheckIcon,
  ArrowRight,
  Sparkles
} from "lucide-react";

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-background/80 backdrop-blur-md border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="font-sans text-xl font-medium tracking-tight">
            <span className="text-foreground">podcast</span>
            <span className="font-light text-gray-500">/</span>
            <span className="text-foreground font-light">clipper</span>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/login">
              <Button variant="ghost">Sign In</Button>
            </Link>
            <Link href="/signup">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-24 text-center">
        <div className="max-w-4xl mx-auto">
          <Badge variant="secondary" className="mb-6">
            <Sparkles className="w-3 h-3 mr-1" />
            AI-Powered Podcast Clipping
          </Badge>
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-8">
            Turn Your Podcasts Into
            <span className="block text-primary">Viral Clips</span>
          </h1>
          <p className="text-xl text-muted-foreground mb-12 max-w-3xl mx-auto leading-relaxed">
            Upload your podcast and let our AI automatically create engaging clips perfect for social media. 
            No editing skills required – just upload, process, and share.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/signup">
              <Button size="lg" className="text-lg px-8 py-6">
                Start Clipping Free
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Button variant="outline" size="lg" className="text-lg px-8 py-6">
              <PlayCircle className="mr-2 h-5 w-5" />
              Watch Demo
            </Button>
          </div>
          <p className="text-sm text-muted-foreground mt-6">
            10 free credits • No credit card required
          </p>
        </div>
      </section>

      {/* How It Works */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">How It Works</h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Transform your long-form content into shareable clips in just three simple steps
          </p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <Card className="text-center">
            <CardHeader>
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Upload className="w-8 h-8 text-primary" />
              </div>
              <CardTitle>1. Upload Your Podcast</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Simply drag and drop your MP4 video file. We support files up to 500MB.
              </p>
            </CardContent>
          </Card>

          <Card className="text-center">
            <CardHeader>
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Scissors className="w-8 h-8 text-primary" />
              </div>
              <CardTitle>2. AI Creates Clips</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Our AI analyzes your content and automatically generates engaging clips optimized for social media.
              </p>
            </CardContent>
          </Card>

          <Card className="text-center">
            <CardHeader>
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Download className="w-8 h-8 text-primary" />
              </div>
              <CardTitle>3. Download & Share</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Download your clips and share them across all your social media platforms to grow your audience.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Features */}
      <section className="bg-muted/30 py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Why Choose Podcast Clipper?</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Powerful features designed to help content creators scale their reach
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <div className="flex flex-col items-start space-y-4">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                <Zap className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold">Lightning Fast Processing</h3>
              <p className="text-muted-foreground">
                Get your clips in minutes, not hours. Our AI processes content quickly and efficiently.
              </p>
            </div>

            <div className="flex flex-col items-start space-y-4">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                <Star className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold">High Quality Output</h3>
              <p className="text-muted-foreground">
                Professional-grade clips optimized for maximum engagement on social platforms.
              </p>
            </div>

            <div className="flex flex-col items-start space-y-4">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                <Clock className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold">Save Hours of Editing</h3>
              <p className="text-muted-foreground">
                No need for complex editing software. We handle all the technical work for you.
              </p>
            </div>

            <div className="flex flex-col items-start space-y-4">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold">AI-Powered Selection</h3>
              <p className="text-muted-foreground">
                Smart algorithms identify the most engaging moments from your content automatically.
              </p>
            </div>

            <div className="flex flex-col items-start space-y-4">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                <Download className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold">Easy Downloads</h3>
              <p className="text-muted-foreground">
                Download all your clips with one click, ready to upload to any platform.
              </p>
            </div>

            <div className="flex flex-col items-start space-y-4">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                <CheckIcon className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold">No Subscriptions</h3>
              <p className="text-muted-foreground">
                Pay only for what you use. Credits never expire, giving you complete flexibility.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Simple, Fair Pricing</h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            No monthly fees or hidden costs. Pay only for the credits you use.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle className="text-2xl">Small Pack</CardTitle>
              <div className="text-4xl font-bold">$9.99</div>
              <p className="text-muted-foreground">Perfect for occasional creators</p>
            </CardHeader>
            <CardContent className="space-y-4">
              <ul className="space-y-3">
                <li className="flex items-center gap-2">
                  <CheckIcon className="w-5 h-5 text-primary" />
                  50 credits
                </li>
                <li className="flex items-center gap-2">
                  <CheckIcon className="w-5 h-5 text-primary" />
                  No expiration
                </li>
                <li className="flex items-center gap-2">
                  <CheckIcon className="w-5 h-5 text-primary" />
                  Download all clips
                </li>
              </ul>
              <Link href="/signup">
                <Button className="w-full" variant="outline">
                  Get Started
                </Button>
              </Link>
            </CardContent>
          </Card>

          <Card className="border-primary border-2 relative">
            <div className="absolute -top-3 left-1/2 -translate-x-1/2">
              <Badge className="bg-primary text-primary-foreground">Most Popular</Badge>
            </div>
            <CardHeader>
              <CardTitle className="text-2xl">Medium Pack</CardTitle>
              <div className="text-4xl font-bold">$24.99</div>
              <Badge variant="secondary" className="w-fit">Save 17%</Badge>
              <p className="text-muted-foreground">Best value for regular podcasters</p>
            </CardHeader>
            <CardContent className="space-y-4">
              <ul className="space-y-3">
                <li className="flex items-center gap-2">
                  <CheckIcon className="w-5 h-5 text-primary" />
                  150 credits
                </li>
                <li className="flex items-center gap-2">
                  <CheckIcon className="w-5 h-5 text-primary" />
                  No expiration
                </li>
                <li className="flex items-center gap-2">
                  <CheckIcon className="w-5 h-5 text-primary" />
                  Download all clips
                </li>
              </ul>
              <Link href="/signup">
                <Button className="w-full">
                  Get Started
                </Button>
              </Link>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-2xl">Large Pack</CardTitle>
              <div className="text-4xl font-bold">$69.99</div>
              <Badge variant="secondary" className="w-fit">Save 30%</Badge>
              <p className="text-muted-foreground">Ideal for studios and agencies</p>
            </CardHeader>
            <CardContent className="space-y-4">
              <ul className="space-y-3">
                <li className="flex items-center gap-2">
                  <CheckIcon className="w-5 h-5 text-primary" />
                  500 credits
                </li>
                <li className="flex items-center gap-2">
                  <CheckIcon className="w-5 h-5 text-primary" />
                  No expiration
                </li>
                <li className="flex items-center gap-2">
                  <CheckIcon className="w-5 h-5 text-primary" />
                  Download all clips
                </li>
              </ul>
              <Link href="/signup">
                <Button className="w-full" variant="outline">
                  Get Started
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>

        <div className="bg-muted/50 rounded-lg p-6 mt-12 max-w-4xl mx-auto">
          <h3 className="text-lg font-semibold mb-4">How credits work</h3>
          <ul className="text-muted-foreground space-y-2 text-sm">
            <li>• 1 credit = 1 minute of podcast processing</li>
            <li>• The program creates around 1 clip per 5 minutes of podcast</li>
            <li>• Credits never expire and can be used anytime</li>
            <li>• All packages are one-time purchases (not subscriptions)</li>
          </ul>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary text-primary-foreground py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-4">Ready to Start Clipping?</h2>
          <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
            Join thousands of content creators who are already growing their audience with AI-powered clips.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/signup">
              <Button size="lg" variant="secondary" className="text-lg px-8 py-6">
                Start Free Trial
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
          </div>
          <p className="text-sm mt-6 opacity-75">
            10 free credits • No credit card required • Start in minutes
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="font-sans text-xl font-medium tracking-tight mb-4">
                <span className="text-foreground">podcast</span>
                <span className="font-light text-gray-500">/</span>
                <span className="text-foreground font-light">clipper</span>
              </div>
              <p className="text-muted-foreground text-sm">
                Transform your podcasts into viral social media clips with the power of AI.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="/features" className="hover:text-foreground">Features</Link></li>
                <li><Link href="/pricing" className="hover:text-foreground">Pricing</Link></li>
                <li><Link href="/demo" className="hover:text-foreground">Demo</Link></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="/help" className="hover:text-foreground">Help Center</Link></li>
                <li><Link href="/contact" className="hover:text-foreground">Contact</Link></li>
                <li><Link href="/status" className="hover:text-foreground">Status</Link></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="/privacy" className="hover:text-foreground">Privacy</Link></li>
                <li><Link href="/terms" className="hover:text-foreground">Terms</Link></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t mt-12 pt-8 text-center text-sm text-muted-foreground">
            <p>&copy; 2025 Podcast Clipper. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;