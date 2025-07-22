"use client";
import {
    ArrowUpIcon,
    Flag,
    Share2,
    MapPin,
    Calendar,
    User,
    BarChart3,
    Brain,
    TrendingUp,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Progress } from "@/components/ui/progress";
import { Report } from "@/lib/types";
import { useAuthStore } from "@/store/authStore";
import {
    Tooltip,
    TooltipContent,
    TooltipTrigger,
} from "@/components/ui/tooltip";
import ReportIssue from "./ReportIssue";
import ReportUpVote from "./ReportUpVote";
import EmailVerificationRequired from "../auth/EmailVerificationRequired";

const ReportActionSide = ({ report }: { report: Report }) => {
    const { isAuthenticated, user } = useAuthStore();

    if (isAuthenticated && !user?.is_verified) {
        return <EmailVerificationRequired action="upvote reports" />;
    }

    // Helper function to format emotion names
    const formatEmotionName = (emotion: string) => {
        return emotion.charAt(0).toUpperCase() + emotion.slice(1);
    };

    // Helper function to get emotion details with proper color classes
    const getEmotionDetails = (emotion: string) => {
        const emotionMap: Record<
            string,
            {
                textColor: string;
                bgColor: string;
                emoji: string;
                description: string;
            }
        > = {
            anger: {
                textColor: "text-red-600",
                bgColor: "bg-red-600",
                emoji: "😠",
                description: "Strong displeasure",
            },
            sadness: {
                textColor: "text-blue-600",
                bgColor: "bg-blue-600",
                emoji: "😢",
                description: "Feeling down",
            },
            fear: {
                textColor: "text-purple-600",
                bgColor: "bg-purple-600",
                emoji: "😨",
                description: "Anxiety or worry",
            },
            joy: {
                textColor: "text-green-600",
                bgColor: "bg-green-600",
                emoji: "😊",
                description: "Positive feeling",
            },
            surprise: {
                textColor: "text-yellow-600",
                bgColor: "bg-yellow-600",
                emoji: "😲",
                description: "Unexpected reaction",
            },
            disgust: {
                textColor: "text-orange-600",
                bgColor: "bg-orange-600",
                emoji: "🤢",
                description: "Strong dislike",
            },
            neutral: {
                textColor: "text-gray-600",
                bgColor: "bg-gray-600",
                emoji: "😐",
                description: "Balanced tone",
            },
        };
        return (
            emotionMap[emotion] || {
                textColor: "text-gray-600",
                bgColor: "bg-gray-600",
                emoji: "😐",
                description: "Unknown emotion",
            }
        );
    };

    return (
        <div className="space-y-6">
            {/* Actions Card */}
            <Card>
                <CardContent className="p-6">
                    <div className="space-y-4">
                        {!isAuthenticated ? (
                            <>
                                <Tooltip>
                                    <TooltipTrigger asChild>
                                        <Button
                                            variant="outline"
                                            className="w-full h-12 text-lg bg-secondary cursor-not-allowed"
                                            size="lg"
                                        >
                                            <ArrowUpIcon className="size-5 mr-3" />
                                            Upvote ({report.up_votes}) 👍
                                        </Button>
                                    </TooltipTrigger>
                                    <TooltipContent>
                                        <p>You must be logged in to upvote</p>
                                    </TooltipContent>
                                </Tooltip>
                                <Tooltip>
                                    <TooltipTrigger asChild>
                                        <Button
                                            variant="outline"
                                            className="w-full h-12 text-lg bg-secondary cursor-not-allowed"
                                            size="lg"
                                        >
                                            <Flag className="size-5 mr-3" />
                                            Report Issue 🚩
                                        </Button>
                                    </TooltipTrigger>
                                    <TooltipContent>
                                        <p>
                                            You must be logged in to report an
                                            issue
                                        </p>
                                    </TooltipContent>
                                </Tooltip>
                            </>
                        ) : (
                            <>
                                <ReportUpVote report={report} />
                                <ReportIssue report={report} />
                            </>
                        )}
                        <Button variant="outline" className="w-full h-12">
                            <Share2 className="h-5 w-5 mr-3" />
                            Share Report
                        </Button>
                    </div>
                </CardContent>
            </Card>

            {/* Report Details Card */}
            <Card>
                <CardHeader className="pb-3">
                    <CardTitle className="text-lg flex items-center gap-2">
                        <BarChart3 className="h-5 w-5" />
                        Report Details 📋
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    {/* Status */}
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-muted-foreground">
                            Status
                        </span>
                        <Badge
                            variant={
                                report.status === "resolved"
                                    ? "default"
                                    : report.status === "in_progress"
                                    ? "secondary"
                                    : report.status === "pending"
                                    ? "outline"
                                    : "destructive"
                            }
                        >
                            {report.status === "resolved" && "✅ "}
                            {report.status === "in_progress" && "⏳ "}
                            {report.status === "pending" && "⏸️ "}
                            {report.status === "rejected" && "❌ "}
                            {report.status.replace("_", " ").toUpperCase()}
                        </Badge>
                    </div>

                    <Separator />

                    {/* Category */}
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-muted-foreground">
                            Category
                        </span>
                        <Badge
                            variant="outline"
                            style={{
                                backgroundColor: `${report.category.color}20`,
                                borderColor: report.category.color,
                            }}
                        >
                            {report.category.name}
                        </Badge>
                    </div>

                    <Separator />

                    {/* Creator */}
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                            <User className="h-4 w-4" />
                            Reported by
                        </span>
                        <span className="text-sm font-medium">
                            {report.created_by.full_name}
                        </span>
                    </div>

                    {/* Date */}
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                            <Calendar className="h-4 w-4" />
                            Created
                        </span>
                        <span className="text-sm">
                            {new Date(report.created_at).toLocaleDateString(
                                "en-US",
                                {
                                    month: "short",
                                    day: "numeric",
                                    year: "numeric",
                                }
                            )}
                        </span>
                    </div>

                    {/* Location */}
                    <div className="flex items-start justify-between">
                        <span className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                            <MapPin className="h-4 w-4" />
                            Location
                        </span>
                        <span className="text-sm text-right max-w-[60%]">
                            {report.address}
                        </span>
                    </div>
                </CardContent>
            </Card>

            {/* Emotion Analysis Card */}
            {report.emotions && report.emotions.length > 0 && (
                <Card>
                    <CardHeader className="pb-3">
                        <CardTitle className="text-lg flex items-center gap-2">
                            <Brain className="h-5 w-5" />
                            Emotion Analysis 🧠
                        </CardTitle>
                        <p className="text-sm text-muted-foreground">
                            AI-detected sentiment from report content 🤖
                        </p>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        {/* Primary Emotion */}
                        <div className="space-y-2">
                            <div className="flex items-center justify-between">
                                <span className="text-sm font-medium flex items-center gap-1">
                                    <TrendingUp className="h-4 w-4" />
                                    Primary Emotion
                                </span>
                                <Badge
                                    variant="outline"
                                    className={
                                        getEmotionDetails(
                                            report.emotions[0].emotion
                                        ).textColor
                                    }
                                >
                                    {
                                        getEmotionDetails(
                                            report.emotions[0].emotion
                                        ).emoji
                                    }{" "}
                                    {formatEmotionName(
                                        report.emotions[0].emotion
                                    )}
                                </Badge>
                            </div>
                            <Progress
                                value={report.emotions[0].score * 100}
                                className="h-2"
                            />
                            <p className="text-xs text-muted-foreground text-right">
                                {(report.emotions[0].score * 100).toFixed(1)}%
                                confidence 📊
                            </p>
                        </div>

                        <Separator />

                        {/* All Emotions Breakdown */}
                        <div className="space-y-3">
                            <h4 className="text-sm font-medium flex items-center gap-1">
                                📈 Emotion Breakdown
                            </h4>
                            <div className="space-y-2">
                                {Object.entries(report.emotions[0].all_emotions)
                                    .sort(([, a], [, b]) => b - a)
                                    .map(([emotion, score]) => {
                                        const emotionDetails =
                                            getEmotionDetails(emotion);
                                        return (
                                            <Tooltip key={emotion}>
                                                <TooltipTrigger asChild>
                                                    <div className="flex items-center justify-between text-sm cursor-help">
                                                        <span
                                                            className={`capitalize ${emotionDetails.textColor} flex items-center gap-1`}
                                                        >
                                                            <span className="text-base">
                                                                {
                                                                    emotionDetails.emoji
                                                                }
                                                            </span>
                                                            {formatEmotionName(
                                                                emotion
                                                            )}
                                                        </span>
                                                        <div className="flex items-center gap-2">
                                                            <div className="w-16 bg-gray-200 dark:bg-gray-700 rounded-full h-1.5">
                                                                <div
                                                                    className={`h-1.5 rounded-full ${emotionDetails.bgColor}`}
                                                                    style={{
                                                                        width: `${
                                                                            score *
                                                                            100
                                                                        }%`,
                                                                    }}
                                                                />
                                                            </div>
                                                            <span className="text-xs text-muted-foreground w-8 text-right">
                                                                {(
                                                                    score * 100
                                                                ).toFixed(0)}
                                                                %
                                                            </span>
                                                        </div>
                                                    </div>
                                                </TooltipTrigger>
                                                <TooltipContent>
                                                    <p>
                                                        {
                                                            emotionDetails.description
                                                        }
                                                    </p>
                                                </TooltipContent>
                                            </Tooltip>
                                        );
                                    })}
                            </div>
                        </div>

                        {/* Content Analysis */}
                        {report.emotions[0].text && (
                            <>
                                <Separator />
                                <div className="space-y-2">
                                    <h4 className="text-sm font-medium flex items-center gap-1">
                                        💬 Analyzed Text
                                    </h4>
                                    <p className="text-xs text-muted-foreground bg-muted p-2 rounded border-l-4 border-blue-500">
                                        "{report.emotions[0].text.content}"
                                    </p>
                                </div>
                            </>
                        )}
                    </CardContent>
                </Card>
            )}
        </div>
    );
};

export default ReportActionSide;
