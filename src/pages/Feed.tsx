import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { TabNavigation } from "@/components/TabNavigation";
import { Clock, DollarSign, MapPin, Star } from "lucide-react";

const mockOrders = [
  {
    id: 1,
    title: "Mobile App UI/UX Design",
    description: "Looking for a talented designer to create a modern mobile app interface for an e-commerce platform. Need clean, user-friendly design with smooth animations.",
    budget: 750,
    timeframe: "2 weeks",
    skills: ["UI/UX", "Figma", "Mobile Design"],
    client: {
      name: "Sarah Chen",
      avatar: "SC",
      rating: 4.9,
      location: "San Francisco, CA"
    },
    postedAt: "2 hours ago",
    proposals: 8
  },
  {
    id: 2,
    title: "Full-Stack Web Development",
    description: "Need an experienced developer to build a modern web application using React and Node.js. The project includes user authentication, real-time features, and payment integration.",
    budget: 2500,
    timeframe: "6 weeks",
    skills: ["React", "Node.js", "MongoDB", "Payment APIs"],
    client: {
      name: "Michael Rodriguez",
      avatar: "MR",
      rating: 4.8,
      location: "Austin, TX"
    },
    postedAt: "4 hours ago",
    proposals: 15
  },
  {
    id: 3,
    title: "Content Writing & SEO",
    description: "Seeking a skilled content writer to create engaging blog posts and optimize them for SEO. Topics include technology, business, and digital marketing.",
    budget: 400,
    timeframe: "1 week",
    skills: ["Content Writing", "SEO", "Digital Marketing"],
    client: {
      name: "Emma Thompson",
      avatar: "ET",
      rating: 4.7,
      location: "London, UK"
    },
    postedAt: "6 hours ago",
    proposals: 12
  },
  {
    id: 4,
    title: "Logo & Brand Identity Design",
    description: "Creating a new brand identity for a tech startup. Need logo design, color palette, typography, and brand guidelines. Looking for modern, professional aesthetic.",
    budget: 600,
    timeframe: "10 days",
    skills: ["Logo Design", "Branding", "Adobe Illustrator"],
    client: {
      name: "David Kim",
      avatar: "DK",
      rating: 5.0,
      location: "Seoul, South Korea"
    },
    postedAt: "8 hours ago",
    proposals: 6
  }
];

export default function Feed() {
  const [selectedOrder, setSelectedOrder] = useState<number | null>(null);

  return (
    <div className="min-h-screen bg-gradient-subtle pb-20">
      {/* Header */}
      <div className="bg-card border-b border-border/50 p-4 sticky top-0 z-40 backdrop-blur-sm">
        <div className="max-w-md mx-auto">
          <h1 className="text-2xl font-bold text-foreground">Available Orders</h1>
          <p className="text-sm text-muted-foreground">Find your next project</p>
        </div>
      </div>

      {/* Orders List */}
      <div className="max-w-md mx-auto p-4 space-y-4">
        {mockOrders.map((order) => (
          <Card key={order.id} className="telegram-card cursor-pointer">
            <CardHeader className="pb-3">
              <div className="flex justify-between items-start gap-3">
                <div className="flex-1">
                  <CardTitle className="text-lg font-semibold text-foreground line-clamp-2">
                    {order.title}
                  </CardTitle>
                  <div className="flex items-center gap-2 mt-2">
                    <Avatar className="h-6 w-6">
                      <AvatarImage src="" />
                      <AvatarFallback className="text-xs bg-primary/10 text-primary">
                        {order.client.avatar}
                      </AvatarFallback>
                    </Avatar>
                    <span className="text-sm text-muted-foreground">{order.client.name}</span>
                    <div className="flex items-center gap-1">
                      <Star size={12} className="text-warning fill-warning" />
                      <span className="text-xs text-muted-foreground">{order.client.rating}</span>
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="flex items-center gap-1 text-success font-semibold">
                    <DollarSign size={16} />
                    ${order.budget}
                  </div>
                  <div className="flex items-center gap-1 text-xs text-muted-foreground mt-1">
                    <Clock size={12} />
                    {order.timeframe}
                  </div>
                </div>
              </div>
            </CardHeader>

            <CardContent className="pt-0 space-y-4">
              <p className="text-sm text-muted-foreground line-clamp-3">
                {order.description}
              </p>

              <div className="flex flex-wrap gap-2">
                {order.skills.map((skill) => (
                  <Badge key={skill} variant="secondary" className="text-xs">
                    {skill}
                  </Badge>
                ))}
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4 text-xs text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <MapPin size={12} />
                    {order.client.location}
                  </div>
                  <span>{order.postedAt}</span>
                  <span>{order.proposals} proposals</span>
                </div>
              </div>

              <Button 
                className="telegram-button w-full"
                onClick={() => setSelectedOrder(order.id)}
              >
                Submit Proposal
              </Button>
            </CardContent>
          </Card>
        ))}

        {/* Load more */}
        <Card className="telegram-card">
          <CardContent className="p-6 text-center">
            <Button variant="outline" className="w-full">
              Load More Orders
            </Button>
          </CardContent>
        </Card>
      </div>
      
      <TabNavigation />
    </div>
  );
}