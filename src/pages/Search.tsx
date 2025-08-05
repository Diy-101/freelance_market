import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { TabNavigation } from "@/components/TabNavigation";
import { Search as SearchIcon, Filter, SlidersHorizontal } from "lucide-react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const categories = [
  "All", "Web Development", "Mobile Apps", "UI/UX Design", 
  "Content Writing", "Digital Marketing", "Data Science", "Blockchain"
];

const budgetRanges = [
  "All Budgets", "$0 - $500", "$500 - $1,500", "$1,500 - $5,000", "$5,000+"
];

export default function Search() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [selectedBudget, setSelectedBudget] = useState("All Budgets");
  const [showFilters, setShowFilters] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-subtle pb-20">
      {/* Header */}
      <div className="bg-card border-b border-border/50 p-4 sticky top-0 z-40 backdrop-blur-sm">
        <div className="max-w-md mx-auto">
          <h1 className="text-2xl font-bold text-foreground">Search Orders</h1>
          <p className="text-sm text-muted-foreground">Find opportunities that match your skills</p>
        </div>
      </div>

      <div className="max-w-md mx-auto p-4 space-y-4">
        {/* Search Input */}
        <Card className="telegram-card">
          <CardContent className="p-4">
            <div className="relative">
              <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground" size={20} />
              <Input
                placeholder="Search projects, skills, or keywords..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 pr-12 h-12 border-0 bg-secondary/50 focus:bg-background transition-colors"
              />
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowFilters(!showFilters)}
                className="absolute right-2 top-1/2 transform -translate-y-1/2 p-2"
              >
                <SlidersHorizontal size={16} />
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Filters */}
        {showFilters && (
          <Card className="telegram-card slide-up">
            <CardContent className="p-4 space-y-4">
              <div className="flex items-center gap-2 mb-3">
                <Filter size={16} className="text-primary" />
                <span className="font-medium">Filters</span>
              </div>

              <div className="space-y-3">
                <div>
                  <label className="text-sm font-medium text-foreground mb-2 block">
                    Category
                  </label>
                  <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                    <SelectTrigger className="w-full">
                      <SelectValue />
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

                <div>
                  <label className="text-sm font-medium text-foreground mb-2 block">
                    Budget Range
                  </label>
                  <Select value={selectedBudget} onValueChange={setSelectedBudget}>
                    <SelectTrigger className="w-full">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {budgetRanges.map((range) => (
                        <SelectItem key={range} value={range}>
                          {range}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="flex gap-2 pt-2">
                <Button variant="outline" className="flex-1">
                  Clear All
                </Button>
                <Button className="telegram-button flex-1">
                  Apply Filters
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Popular Categories */}
        <Card className="telegram-card">
          <CardContent className="p-4">
            <h3 className="font-semibold text-foreground mb-3">Popular Categories</h3>
            <div className="flex flex-wrap gap-2">
              {categories.slice(1, 7).map((category) => (
                <Badge
                  key={category}
                  variant="secondary"
                  className="cursor-pointer hover:bg-primary hover:text-primary-foreground transition-colors"
                  onClick={() => setSelectedCategory(category)}
                >
                  {category}
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Quick Search Suggestions */}
        <Card className="telegram-card">
          <CardContent className="p-4">
            <h3 className="font-semibold text-foreground mb-3">Quick Searches</h3>
            <div className="space-y-2">
              {[
                "React Developer",
                "Logo Design",
                "Content Writer",
                "SEO Expert",
                "Mobile App Developer",
                "Social Media Manager"
              ].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => setSearchQuery(suggestion)}
                  className="w-full text-left p-3 rounded-lg bg-secondary/30 hover:bg-secondary/50 transition-colors text-sm"
                >
                  <SearchIcon size={14} className="inline mr-2 text-muted-foreground" />
                  {suggestion}
                </button>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Search Results Placeholder */}
        {searchQuery && (
          <Card className="telegram-card">
            <CardContent className="p-6 text-center">
              <SearchIcon size={48} className="mx-auto text-muted-foreground mb-4" />
              <h3 className="font-semibold text-foreground mb-2">
                Searching for "{searchQuery}"
              </h3>
              <p className="text-sm text-muted-foreground">
                Please wait while we find the best matches for you...
              </p>
            </CardContent>
          </Card>
        )}
      </div>
      
      <TabNavigation />
    </div>
  );
}