import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { TabNavigation } from "@/components/TabNavigation";
import { 
  Clock, 
  DollarSign, 
  CheckCircle, 
  AlertCircle, 
  MessageSquare,
  Calendar,
  Play,
  Pause
} from "lucide-react";

const activeJobs = [
  {
    id: 1,
    title: "E-commerce Website Redesign",
    client: "TechCorp Inc.",
    clientAvatar: "TC",
    budget: 2500,
    progress: 65,
    deadline: "Dec 15, 2024",
    status: "in-progress",
    description: "Redesigning the entire user interface for better user experience",
    timeTracked: "28 hours"
  },
  {
    id: 2,
    title: "Mobile App Development",
    client: "StartupXYZ",
    clientAvatar: "SX",
    budget: 4000,
    progress: 30,
    deadline: "Jan 20, 2025",
    status: "in-progress",
    description: "Building a React Native app for iOS and Android",
    timeTracked: "42 hours"
  }
];

const completedJobs = [
  {
    id: 3,
    title: "Logo Design Package",
    client: "Creative Agency",
    clientAvatar: "CA",
    budget: 800,
    completedDate: "Nov 28, 2024",
    rating: 5,
    earnings: 800,
    feedback: "Excellent work! Very professional and delivered on time."
  },
  {
    id: 4,
    title: "Content Writing Project",
    client: "Marketing Pro",
    clientAvatar: "MP",
    budget: 600,
    completedDate: "Nov 15, 2024",
    rating: 4.8,
    earnings: 600,
    feedback: "Great quality content. Would hire again!"
  }
];

const proposals = [
  {
    id: 5,
    title: "Web Development Project",
    submittedDate: "Dec 1, 2024",
    proposedBudget: 1800,
    status: "pending",
    client: "Digital Solutions"
  },
  {
    id: 6,
    title: "UI/UX Design Task",
    submittedDate: "Nov 30, 2024",
    proposedBudget: 1200,
    status: "declined",
    client: "Design Studio"
  }
];

export default function MyJobs() {
  const [activeTab, setActiveTab] = useState("active");

  const getStatusColor = (status: string) => {
    switch (status) {
      case "in-progress": return "text-primary";
      case "completed": return "text-success";
      case "pending": return "text-warning";
      case "declined": return "text-destructive";
      default: return "text-muted-foreground";
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "in-progress": return <Badge className="bg-primary/10 text-primary">In Progress</Badge>;
      case "completed": return <Badge className="bg-success/10 text-success">Completed</Badge>;
      case "pending": return <Badge className="bg-warning/10 text-warning">Pending</Badge>;
      case "declined": return <Badge className="bg-destructive/10 text-destructive">Declined</Badge>;
      default: return <Badge variant="secondary">{status}</Badge>;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-subtle pb-20">
      {/* Header */}
      <div className="bg-card border-b border-border/50 p-4 sticky top-0 z-40 backdrop-blur-sm">
        <div className="max-w-md mx-auto">
          <h1 className="text-2xl font-bold text-foreground">My Jobs</h1>
          <p className="text-sm text-muted-foreground">Track your projects and earnings</p>
        </div>
      </div>

      <div className="max-w-md mx-auto p-4">
        {/* Quick Stats */}
        <Card className="telegram-card mb-4">
          <CardContent className="p-4">
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <div className="text-lg font-bold text-primary">{activeJobs.length}</div>
                <div className="text-xs text-muted-foreground">Active</div>
              </div>
              <div>
                <div className="text-lg font-bold text-success">{completedJobs.length}</div>
                <div className="text-xs text-muted-foreground">Completed</div>
              </div>
              <div>
                <div className="text-lg font-bold text-warning">{proposals.length}</div>
                <div className="text-xs text-muted-foreground">Proposals</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="active">Active</TabsTrigger>
            <TabsTrigger value="completed">Completed</TabsTrigger>
            <TabsTrigger value="proposals">Proposals</TabsTrigger>
          </TabsList>

          {/* Active Jobs */}
          <TabsContent value="active" className="space-y-4 mt-4">
            {activeJobs.map((job) => (
              <Card key={job.id} className="telegram-card">
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <CardTitle className="text-lg font-semibold">{job.title}</CardTitle>
                      <div className="flex items-center gap-2 mt-1">
                        <Avatar className="h-5 w-5">
                          <AvatarFallback className="text-xs bg-primary/10 text-primary">
                            {job.clientAvatar}
                          </AvatarFallback>
                        </Avatar>
                        <span className="text-sm text-muted-foreground">{job.client}</span>
                      </div>
                    </div>
                    {getStatusBadge(job.status)}
                  </div>
                </CardHeader>

                <CardContent className="space-y-4">
                  <p className="text-sm text-muted-foreground">{job.description}</p>

                  {/* Progress Bar */}
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Progress</span>
                      <span>{job.progress}%</span>
                    </div>
                    <div className="w-full bg-secondary rounded-full h-2">
                      <div 
                        className="bg-primary h-2 rounded-full transition-all duration-300"
                        style={{ width: `${job.progress}%` }}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div className="flex items-center gap-2">
                      <DollarSign size={14} className="text-success" />
                      <span>${job.budget}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Calendar size={14} className="text-warning" />
                      <span>{job.deadline}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Clock size={14} className="text-primary" />
                      <span>{job.timeTracked}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <MessageSquare size={14} className="text-muted-foreground" />
                      <span>3 messages</span>
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <Button variant="outline" size="sm" className="flex-1">
                      <MessageSquare size={14} className="mr-1" />
                      Message
                    </Button>
                    <Button size="sm" className="flex-1">
                      <Play size={14} className="mr-1" />
                      Continue
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </TabsContent>

          {/* Completed Jobs */}
          <TabsContent value="completed" className="space-y-4 mt-4">
            {completedJobs.map((job) => (
              <Card key={job.id} className="telegram-card">
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <CardTitle className="text-lg font-semibold">{job.title}</CardTitle>
                      <div className="flex items-center gap-2 mt-1">
                        <Avatar className="h-5 w-5">
                          <AvatarFallback className="text-xs bg-primary/10 text-primary">
                            {job.clientAvatar}
                          </AvatarFallback>
                        </Avatar>
                        <span className="text-sm text-muted-foreground">{job.client}</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold text-success">${job.earnings}</div>
                      <div className="text-xs text-muted-foreground">Earned</div>
                    </div>
                  </div>
                </CardHeader>

                <CardContent className="space-y-3">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Completed:</span>
                    <span>{job.completedDate}</span>
                  </div>
                  
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Rating:</span>
                    <div className="flex items-center gap-1">
                      <span className="font-medium">{job.rating}</span>
                      <div className="flex">
                        {[...Array(5)].map((_, i) => (
                          <span
                            key={i}
                            className={`text-xs ${
                              i < Math.floor(job.rating) ? 'text-warning' : 'text-muted-foreground'
                            }`}
                          >
                            ★
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  {job.feedback && (
                    <div className="p-3 bg-secondary/30 rounded-lg">
                      <p className="text-sm italic">"{job.feedback}"</p>
                    </div>
                  )}

                  <Button variant="outline" className="w-full" size="sm">
                    View Details
                  </Button>
                </CardContent>
              </Card>
            ))}
          </TabsContent>

          {/* Proposals */}
          <TabsContent value="proposals" className="space-y-4 mt-4">
            {proposals.map((proposal) => (
              <Card key={proposal.id} className="telegram-card">
                <CardContent className="p-4">
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex-1">
                      <h3 className="font-semibold">{proposal.title}</h3>
                      <p className="text-sm text-muted-foreground">{proposal.client}</p>
                    </div>
                    {getStatusBadge(proposal.status)}
                  </div>

                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-muted-foreground">Proposed:</span>
                      <div className="font-medium">${proposal.proposedBudget}</div>
                    </div>
                    <div>
                      <span className="text-muted-foreground">Submitted:</span>
                      <div className="font-medium">{proposal.submittedDate}</div>
                    </div>
                  </div>

                  {proposal.status === "pending" && (
                    <Button variant="outline" className="w-full mt-3" size="sm">
                      View Proposal
                    </Button>
                  )}
                </CardContent>
              </Card>
            ))}
          </TabsContent>
        </Tabs>
      </div>
      
      <TabNavigation />
    </div>
  );
}