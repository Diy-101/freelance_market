import { useState } from "react";
import { Button } from "@heroui/react";
import { ChevronRight, Users, Clock, ShieldCheck } from "lucide-react";
import deal_duck from "@/assets/stickers/deal_duck.json";
import fast_duck from "@/assets/stickers/fast_duck.json";
import money_duck from "@/assets/stickers/money_duck.json";
import test from "@/assets/stickers/flame.json";
import StickerPlayer from "./StickerPlayer";
import { Card, CardHeader, CardBody, CardFooter } from "@heroui/react";
interface OnboardingFlowProps {
  onComplete: () => void;
}

const onboardingCards = [
  {
    id: 1,
    animation: deal_duck,
    title: "Find Perfect Freelancers",
    description:
      "Connect with skilled professionals from around the world. Browse profiles, reviews, and portfolios to find the perfect match for your project.",
    color: "text-primary",
  },
  {
    id: 2,
    animation: fast_duck,
    title: "Fast & Efficient",
    description:
      "Get your projects completed quickly with our streamlined process. Real-time communication and milestone tracking keep everything on schedule.",
    color: "text-success",
  },
  {
    id: 3,
    animation: money_duck,
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
  return (
    <div className="min-h-screen bg-gradient-subtle flex flex-col items-center justify-center p-6">
      <Card className="telegram-card w-full max-w-md mx-auto flex flex-1 flex-col">
        {/* Progress indicators */}
        <CardHeader className="flex flex-1 items-start justify-center">
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
        </CardHeader>
        <CardBody className="flex flex-col overflow-visible py-2 gap-32">
          <StickerPlayer key={card.id} animationData={card.animation} />
          <div className="space-y-3 mt-16">
            <h2 className="text-2xl font-bold text-foreground">{card.title}</h2>
            <p className="text-muted-foreground leading-relaxed">
              {card.description}
            </p>
          </div>
        </CardBody>
        <CardFooter className="flex-1 flex items-end">
          <div className="space-y-4 flex-1">
            <Button
              onPress={nextCard}
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
        </CardFooter>
      </Card>
    </div>
  );
};
