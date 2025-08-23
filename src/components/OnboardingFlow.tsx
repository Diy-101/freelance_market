import { useState } from "react";
import { Button } from "@heroui/react";
import { Card, CardHeader, CardBody, CardFooter } from "@heroui/react";
import { useLanguage } from "@/hooks/useLanguage";
import modern_duck from "@/assets/stickers/modern_duck.json";
import fast_duck from "@/assets/stickers/fast_duck.json";
import money_duck from "@/assets/stickers/money_duck.json";
import StickerPlayer from "@/components/StickerPlayer";

interface OnboardingFlowProps {
  onComplete: () => void;
}

const onboardingCards = [
  {
    id: 1,
    animation: modern_duck,
  },
  {
    id: 2,
    animation: fast_duck,
  },
  {
    id: 3,
    animation: money_duck,
  },
];

export const OnboardingFlow = ({ onComplete }: OnboardingFlowProps) => {
  const [currentCard, setCurrentCard] = useState(0);
  const { t } = useLanguage();

  const translations = t();

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
      <Card
        key={card.id}
        className="telegram-card w-full max-w-md mx-auto flex flex-1 flex-col"
      >
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
            <h2 className="text-2xl font-bold text-foreground">
              {translations.onboarding[currentCard].title}
            </h2>
            <p className="text-muted-foreground leading-relaxed">
              {translations.onboarding[currentCard].description}
            </p>
          </div>
        </CardBody>

        <CardFooter className="flex-1 flex items-end">
          <div className="space-y-4 flex-1">
            <Button
              onPress={nextCard}
              className="telegram-button w-full h-12 text-lg"
            >
              {translations.onboarding[currentCard].button}
            </Button>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
};
