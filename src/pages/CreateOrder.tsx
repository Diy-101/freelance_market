import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { TabNavigation } from "@/components/TabNavigation";
import { Plus, X, DollarSign, Clock, FileText } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const categories = [
  "Web Development", "Mobile Apps", "UI/UX Design", 
  "Content Writing", "Digital Marketing", "Data Science", "Blockchain"
];

const timeframes = [
  "Less than 1 week", "1-2 weeks", "2-4 weeks", "1-3 months", "3+ months"
];

export default function CreateOrder() {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    category: "",
    budget: "",
    timeframe: "",
    skills: [] as string[],
  });
  const [newSkill, setNewSkill] = useState("");

  const addSkill = () => {
    if (newSkill.trim() && !formData.skills.includes(newSkill.trim())) {
      setFormData({
        ...formData,
        skills: [...formData.skills, newSkill.trim()]
      });
      setNewSkill("");
    }
  };

  const removeSkill = (skillToRemove: string) => {
    setFormData({
      ...formData,
      skills: formData.skills.filter(skill => skill !== skillToRemove)
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.title || !formData.description || !formData.category || !formData.budget) {
      toast({
        title: "Missing Information",
        description: "Please fill in all required fields",
        variant: "destructive"
      });
      return;
    }

    toast({
      title: "Order Created Successfully!",
      description: "Your project has been posted and freelancers can now submit proposals.",
    });
    
    navigate("/feed");
  };

  return (
    <div className="min-h-screen bg-gradient-subtle pb-20">
      {/* Header */}
      <div className="bg-card border-b border-border/50 p-4 sticky top-0 z-40 backdrop-blur-sm">
        <div className="max-w-md mx-auto">
          <h1 className="text-2xl font-bold text-foreground">Create New Order</h1>
          <p className="text-sm text-muted-foreground">Post your project and get proposals</p>
        </div>
      </div>

      <div className="max-w-md mx-auto p-4 space-y-4">
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Project Title */}
          <Card className="telegram-card">
            <CardHeader className="pb-3">
              <CardTitle className="text-lg flex items-center gap-2">
                <FileText size={20} className="text-primary" />
                Project Details
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="title" className="text-sm font-medium">
                  Project Title *
                </Label>
                <Input
                  id="title"
                  placeholder="e.g. Build a modern e-commerce website"
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="description" className="text-sm font-medium">
                  Project Description *
                </Label>
                <Textarea
                  id="description"
                  placeholder="Describe your project in detail. Include requirements, expectations, and any specific preferences..."
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  className="mt-1 min-h-[100px]"
                />
              </div>

              <div>
                <Label htmlFor="category" className="text-sm font-medium">
                  Category *
                </Label>
                <Select onValueChange={(value) => setFormData({...formData, category: value})}>
                  <SelectTrigger className="mt-1">
                    <SelectValue placeholder="Select a category" />
                  </SelectTrigger>
                  <SelectContent>
                    {categories.map((category) => (
                      <SelectItem key={category} value={category}>
                        {category}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Budget & Timeline */}
          <Card className="telegram-card">
            <CardHeader className="pb-3">
              <CardTitle className="text-lg flex items-center gap-2">
                <DollarSign size={20} className="text-success" />
                Budget & Timeline
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="budget" className="text-sm font-medium">
                  Budget (USD) *
                </Label>
                <Input
                  id="budget"
                  type="number"
                  placeholder="1000"
                  value={formData.budget}
                  onChange={(e) => setFormData({...formData, budget: e.target.value})}
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="timeframe" className="text-sm font-medium">
                  Expected Timeframe
                </Label>
                <Select onValueChange={(value) => setFormData({...formData, timeframe: value})}>
                  <SelectTrigger className="mt-1">
                    <SelectValue placeholder="Select timeframe" />
                  </SelectTrigger>
                  <SelectContent>
                    {timeframes.map((timeframe) => (
                      <SelectItem key={timeframe} value={timeframe}>
                        {timeframe}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Skills Required */}
          <Card className="telegram-card">
            <CardHeader className="pb-3">
              <CardTitle className="text-lg">Required Skills</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex gap-2">
                <Input
                  placeholder="Add a skill (e.g. React, Design, Writing)"
                  value={newSkill}
                  onChange={(e) => setNewSkill(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addSkill())}
                  className="flex-1"
                />
                <Button
                  type="button"
                  onClick={addSkill}
                  size="sm"
                  className="px-3"
                >
                  <Plus size={16} />
                </Button>
              </div>

              {formData.skills.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {formData.skills.map((skill) => (
                    <Badge
                      key={skill}
                      variant="secondary"
                      className="flex items-center gap-1"
                    >
                      {skill}
                      <button
                        type="button"
                        onClick={() => removeSkill(skill)}
                        className="hover:text-destructive"
                      >
                        <X size={12} />
                      </button>
                    </Badge>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Submit Button */}
          <Card className="telegram-card">
            <CardContent className="p-4">
              <Button type="submit" className="telegram-button w-full h-12">
                Post Project
              </Button>
              <p className="text-xs text-muted-foreground text-center mt-2">
                By posting, you agree to our terms of service
              </p>
            </CardContent>
          </Card>
        </form>
      </div>
      
      <TabNavigation />
    </div>
  );
}