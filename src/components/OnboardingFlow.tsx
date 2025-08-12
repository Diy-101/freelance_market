import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { ChevronRight, Users, Clock, ShieldCheck } from "lucide-react";
import "@lottiefiles/lottie-player";

interface OnboardingFlowProps {
  onComplete: () => void;
}

const onboardingCards = [
  {
    icon: Users,
    title: "Find Perfect Freelancers",
    description:
      "Connect with skilled professionals from around the world. Browse profiles, reviews, and portfolios to find the perfect match for your project.",
    color: "text-primary",
  },
  {
    icon: Clock,
    title: "Fast & Efficient",
    description:
      "Get your projects completed quickly with our streamlined process. Real-time communication and milestone tracking keep everything on schedule.",
    color: "text-success",
  },
  {
    icon: ShieldCheck,
    title: "0% Commission",
    description:
      "Keep 100% of your earnings! No hidden fees, no commission charges. What you earn is what you keep. Fair pricing for everyone.",
    color: "text-warning",
  },
];

export const OnboardingFlow = ({ onComplete }: OnboardingFlowProps) => {
  const [currentCard, setCurrentCard] = useState(0);

  const nextCard = () => {
    if (currentCard < onboardingCards.length - 1) {
      setCurrentCard(currentCard + 1);
    } else {
      onComplete();
    }
  };
  const card = onboardingCards[currentCard];
  const Icon = card.icon;

  return (
    <div className="min-h-screen bg-gradient-subtle flex flex-col justify-center p-6">
      <div className="max-w-md mx-auto w-full space-y-8">
        {/* Progress indicators */}
        <div className="flex justify-center space-x-2">
          {onboardingCards.map((_, index) => (
            <div
              key={index}
              className={`h-2 w-8 rounded-full transition-all duration-300 ${
                index <= currentCard ? "bg-primary" : "bg-border"
              }`}
            />
          ))}
        </div>

        {/* Card */}
        <Card className="telegram-card slide-up">
          <CardContent className="p-8 text-center space-y-6">
            <div
              className={`inline-flex p-4 rounded-2xl bg-secondary/50 ${card.color}`}
            >
              <Icon size={32} />
            </div>

            <div className="space-y-3">
              <h2 className="text-2xl font-bold text-foreground">
                {card.title}
              </h2>

              {/* Стикер под заголовком */}
              <div className="my-4 flex justify-center">
                <tgs-player
                  autoplay
                  loop
                  mode="normal"
                  src="/stickers/flame.tgs"
                ></tgs-player>
              </div>

              <p className="text-muted-foreground leading-relaxed">
                {card.description}
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Action buttons */}
        <div className="space-y-4">
          <Button
            onClick={nextCard}
            className="telegram-button w-full h-12 text-lg"
          >
            {currentCard === onboardingCards.length - 1 ? (
              "Get Started"
            ) : (
              <span className="flex items-center justify-center gap-2">
                Continue <ChevronRight size={20} />
              </span>
            )}
          </Button>
        </div>

        {/* App title */}
        <div className="text-center fade-in">
          <h1 className="text-3xl font-bold bg-gradient-primary bg-clip-text text-transparent">
            FreelanceHub
          </h1>
          <p className="text-sm text-muted-foreground mt-1">
            Your gateway to limitless opportunities
          </p>
        </div>
      </div>
    </div>
  );
};
