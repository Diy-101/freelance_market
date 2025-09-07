import React from "react";
import Lottie from "react-lottie-player";

interface StickerPlayerProps {
  animationData: any;
  className?: string;
}

const StickerPlayer: React.FC<StickerPlayerProps> = ({
  animationData,
  className = "",
}) => {
  return (
    <div className={`flex justify-center ${className}`}>
      <Lottie
        loop
        animationData={animationData}
        play
        className="w-full h-full"
      />
    </div>
  );
};

export default StickerPlayer;
