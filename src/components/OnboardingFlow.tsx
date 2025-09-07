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
    <div className="min-h-screen bg-gradient-subtle flex flex-col items-center justify-center p-4">
      <Card
        key={card.id}
        className="telegram-card w-full max-w-md max-h-screen mx-auto flex flex-col overflow-hidden"
      >
        {/* Progress indicators */}
        <CardHeader className="flex justify-center py-2">
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

        <CardBody className="flex flex-col flex-1 overflow-auto py-4 gap-6">
          <div className="flex justify-center">
            <StickerPlayer
              key={card.id}
              animationData={card.animation}
              className="max-w-full h-auto"
            />
          </div>

          <div className="space-y-2 mt-4 px-2 text-center">
            <h2 className="text-xl sm:text-2xl font-bold text-foreground">
              {translations.onboarding[currentCard].title}
            </h2>
            <p className="text-sm sm:text-base text-muted-foreground leading-relaxed">
              {translations.onboarding[currentCard].description}
            </p>
          </div>
        </CardBody>

        <CardFooter className="flex justify-center py-4">
          <Button
            onPress={nextCard}
            className="telegram-button w-full max-w-xs h-12 text-lg"
          >
            {translations.onboarding[currentCard].button}
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
};
