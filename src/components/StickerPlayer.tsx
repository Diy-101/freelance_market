import React from "react";
import Lottie from "react-lottie-player";

interface StickerPlayerProps {
  animationData: any; // сюда передаём JSON-анимацию
  width?: number; //em
  height?: number; //em
}

const StickerPlayer: React.FC<StickerPlayerProps> = ({
  animationData,
  width = 9,
  height = 9,
}) => {
  return (
    <Lottie
      loop={true}
      animationData={animationData}
      play={true}
      style={{ width: `${width}em`, height: `${height}em`, margin: "0 auto" }}
    />
  );
};

export default StickerPlayer;
