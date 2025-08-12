import React from "react";
import Lottie from "react-lottie-player";

interface StickerPlayerProps {
  animationData: any; // сюда передаём JSON-анимацию
  width?: number;
  height?: number;
}

const StickerPlayer: React.FC<StickerPlayerProps> = ({
  animationData,
  width = 150,
  height = 150,
}) => {
  return (
    <Lottie
      loop
      animationData={animationData}
      play
      style={{ width, height, margin: "0 auto" }}
    />
  );
};

export default StickerPlayer;
