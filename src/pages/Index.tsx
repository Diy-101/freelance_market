import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { OnboardingFlow } from "@/components/OnboardingFlow";
import { TabNavigation } from "@/components/TabNavigation";

const Index = () => {
  const navigate = useNavigate();
  const [showOnboarding, setShowOnboarding] = useState(true);

  useEffect(() => {
    // Check if user has completed onboarding before
    const hasCompletedOnboarding = localStorage.getItem("onboarding-completed");
    if (hasCompletedOnboarding) {
      setShowOnboarding(false);
      navigate("/feed");
    }
  }, [navigate]);

  const handleOnboardingComplete = () => {
    localStorage.setItem("onboarding-completed", "true");
    setShowOnboarding(false);
    navigate("/feed");
  };

  if (showOnboarding) {
    return <OnboardingFlow onComplete={handleOnboardingComplete} />;
  }

  return (
    <div className="min-h-screen bg-gradient-subtle">
      <TabNavigation />
    </div>
  );
};

export default Index;
