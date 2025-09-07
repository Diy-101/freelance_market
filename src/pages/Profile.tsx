import { useState, useRef, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@heroui/react";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { TabNavigation } from "@/components/TabNavigation";
import {
  User,
  Star,
  MapPin,
  Calendar,
  DollarSign,
  Briefcase,
  Edit3,
  Settings,
  Shield,
  Award,
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export default function Profile() {
  const { toast } = useToast();
  const [isEditing, setIsEditing] = useState(false);
  const [isEmployeeMode, setIsEmployeeMode] = useState(false);
  const changeProfileRef = useRef(null);
  const defaultPositionRef = useRef(null);

  const [profileData, setProfileData] = useState({
    name: "Alex Johnson",
    bio: "Full-stack developer with 5+ years of experience in React, Node.js, and cloud technologies.",
    location: "New York, USA",
    hourlyRate: 45,
    skills: ["React", "Node.js", "TypeScript", "AWS", "MongoDB"],
    completedProjects: 47,
    rating: 4.9,
    totalEarnings: 12450,
  });

  const [employeeProfile, setEmployeeProfile] = useState({
    portfolio: "",
    experience: "",
    availability: "full-time",
    certifications: [] as string[],
  });

  const handleSaveProfile = () => {
    toast({
      title: "Profile Updated",
      description: "Your profile has been successfully updated.",
    });
    setIsEditing(false);
  };

  const toggleEmployeeMode = () => {
    setIsEmployeeMode(!isEmployeeMode);
    if (!isEmployeeMode) {
      toast({
        title: "Employee Mode Activated",
        description:
          "You can now receive job invitations and apply to projects.",
      });
    }
  };

  useEffect(() => {
    if (isEditing) {
      changeProfileRef.current.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    } else {
      defaultPositionRef.current.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }, [isEditing]);

  return (
    <div
      ref={defaultPositionRef}
      className="min-h-screen bg-gradient-subtle pb-20"
    >
      <div className="max-w-md mx-auto p-4 space-y-4">
        {/* Profile Header */}
        <Card className="telegram-card">
          <CardContent className="p-6">
            <div className="flex items-start gap-4">
              <Avatar className="h-16 w-16">
                <AvatarImage src="" />
                <AvatarFallback className="bg-primary text-primary-foreground text-lg">
                  AJ
                </AvatarFallback>
              </Avatar>

              <div className="flex-1">
                <div className="flex justify-between items-start">
                  <div>
                    <h2 className="text-xl font-bold text-foreground">
                      {profileData.name}
                    </h2>
                    <div className="flex items-center gap-2 mt-1">
                      <div className="flex items-center gap-1">
                        <Star size={14} className="text-warning fill-warning" />
                        <span className="text-sm font-medium">
                          {profileData.rating}
                        </span>
                      </div>
                      <span className="text-sm text-muted-foreground">
                        ({profileData.completedProjects} projects)
                      </span>
                    </div>
                  </div>
                  <Button size="sm" onClick={() => setIsEditing(!isEditing)}>
                    <Edit3 size={16} />
                  </Button>
                </div>

                <div className="flex items-center gap-1 mt-2 text-sm text-muted-foreground">
                  <MapPin size={14} />
                  {profileData.location}
                </div>
              </div>
            </div>

            <p className="text-sm text-muted-foreground mt-4">
              {profileData.bio}
            </p>

            <div className="flex gap-4 mt-4 pt-4 border-t border-border/50">
              <div className="text-center">
                <div className="text-lg font-bold text-success">
                  ${profileData.totalEarnings}
                </div>
                <div className="text-xs text-muted-foreground">
                  Total Earned
                </div>
              </div>
              <div className="text-center">
                <div className="text-lg font-bold text-primary">
                  {profileData.completedProjects}
                </div>
                <div className="text-xs text-muted-foreground">Projects</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-bold text-warning">
                  {profileData.rating}
                </div>
                <div className="text-xs text-muted-foreground">Rating</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Employee Mode Toggle */}
        <Card className="telegram-card">
          <CardContent className="p-4">
            <div className="flex justify-between items-center">
              <div>
                <h3 className="font-semibold text-foreground">Employee Mode</h3>
                <p className="text-sm text-muted-foreground">
                  {isEmployeeMode
                    ? "You're available for hire"
                    : "Enable to receive job invitations"}
                </p>
              </div>
              <Button
                onClick={toggleEmployeeMode}
                className={isEmployeeMode ? "telegram-button" : ""}
              >
                {isEmployeeMode ? "Active" : "Enable"}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Profile Tabs */}
        <Tabs defaultValue="info" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="info">Info</TabsTrigger>
            <TabsTrigger value="skills">Skills</TabsTrigger>
            <TabsTrigger value="stats">Stats</TabsTrigger>
          </TabsList>

          <TabsContent value="info" className="space-y-4">
            <Card className="telegram-card">
              <CardHeader>
                <CardTitle className="text-lg">Personal Information</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {isEditing ? (
                  <div ref={changeProfileRef}>
                    <div>
                      <Label htmlFor="name">Full Name</Label>
                      <Input
                        id="name"
                        value={profileData.name}
                        onChange={(e) =>
                          setProfileData({
                            ...profileData,
                            name: e.target.value,
                          })
                        }
                      />
                    </div>
                    <div>
                      <Label htmlFor="bio">Bio</Label>
                      <Textarea
                        id="bio"
                        value={profileData.bio}
                        onChange={(e) =>
                          setProfileData({
                            ...profileData,
                            bio: e.target.value,
                          })
                        }
                      />
                    </div>
                    <div>
                      <Label htmlFor="location">Location</Label>
                      <Input
                        id="location"
                        value={profileData.location}
                        onChange={(e) =>
                          setProfileData({
                            ...profileData,
                            location: e.target.value,
                          })
                        }
                      />
                    </div>
                    <div>
                      <Label htmlFor="rate">Hourly Rate ($)</Label>
                      <Input
                        id="rate"
                        type="number"
                        value={profileData.hourlyRate}
                        onChange={(e) =>
                          setProfileData({
                            ...profileData,
                            hourlyRate: Number(e.target.value),
                          })
                        }
                      />
                    </div>
                    <div className="flex gap-2">
                      <Button
                        onClick={handleSaveProfile}
                        className="telegram-button flex-1"
                      >
                        Save Changes
                      </Button>
                      <Button
                        onClick={() => setIsEditing(false)}
                        className="flex-1"
                      >
                        Cancel
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">
                        Hourly Rate:
                      </span>
                      <span className="font-medium">
                        ${profileData.hourlyRate}/hour
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">
                        Member Since:
                      </span>
                      <span className="font-medium">January 2023</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">
                        Response Time:
                      </span>
                      <span className="font-medium">Within 2 hours</span>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Employee Profile Section */}
            {isEmployeeMode && (
              <Card className="telegram-card">
                <CardHeader>
                  <CardTitle className="text-lg flex items-center gap-2">
                    <Briefcase size={18} className="text-primary" />
                    Employee Profile
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label htmlFor="portfolio">Portfolio URL</Label>
                    <Input
                      id="portfolio"
                      placeholder="https://your-portfolio.com"
                      value={employeeProfile.portfolio}
                      onChange={(e) =>
                        setEmployeeProfile({
                          ...employeeProfile,
                          portfolio: e.target.value,
                        })
                      }
                    />
                  </div>
                  <div>
                    <Label htmlFor="experience">Experience Summary</Label>
                    <Textarea
                      id="experience"
                      placeholder="Describe your professional experience..."
                      value={employeeProfile.experience}
                      onChange={(e) =>
                        setEmployeeProfile({
                          ...employeeProfile,
                          experience: e.target.value,
                        })
                      }
                    />
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          <TabsContent value="skills" className="space-y-4">
            <Card className="telegram-card">
              <CardHeader>
                <CardTitle className="text-lg">Skills & Expertise</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {profileData.skills.map((skill) => (
                    <Badge key={skill} variant="secondary" className="text-sm">
                      {skill}
                    </Badge>
                  ))}
                </div>
                <Button className="w-full mt-4">Add More Skills</Button>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="stats" className="space-y-4">
            <Card className="telegram-card">
              <CardHeader>
                <CardTitle className="text-lg">Performance Stats</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-3 bg-secondary/30 rounded-lg">
                    <DollarSign
                      className="mx-auto text-success mb-2"
                      size={20}
                    />
                    <div className="font-bold">
                      ${profileData.totalEarnings}
                    </div>
                    <div className="text-xs text-muted-foreground">
                      Total Earned
                    </div>
                  </div>
                  <div className="text-center p-3 bg-secondary/30 rounded-lg">
                    <Briefcase
                      className="mx-auto text-primary mb-2"
                      size={20}
                    />
                    <div className="font-bold">
                      {profileData.completedProjects}
                    </div>
                    <div className="text-xs text-muted-foreground">
                      Completed
                    </div>
                  </div>
                  <div className="text-center p-3 bg-secondary/30 rounded-lg">
                    <Star className="mx-auto text-warning mb-2" size={20} />
                    <div className="font-bold">{profileData.rating}</div>
                    <div className="text-xs text-muted-foreground">Rating</div>
                  </div>
                  <div className="text-center p-3 bg-secondary/30 rounded-lg">
                    <Award className="mx-auto text-success mb-2" size={20} />
                    <div className="font-bold">98%</div>
                    <div className="text-xs text-muted-foreground">
                      Success Rate
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>

      <TabNavigation />
    </div>
  );
}
