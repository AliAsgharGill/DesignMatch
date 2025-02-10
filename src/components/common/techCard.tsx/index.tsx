import Image from "next/image";
import React from "react";
import { TechCardProps } from "./types";

const TechCard: React.FC<TechCardProps> = ({
  logo,
  name,
  width,
  height,
  className = "",
  colorFrom,
  colorTo,
  imageWidth,
  imageHeight,
  grayscale = "grayscale",
}) => {
  return (
    <div
      className={`group relative flex items-center justify-center rounded-lg transition-all hover:border-transparent shadow-lg shadow-shadowPrimary ${width} ${height} ${className}`}
    >
      {/* Gradient Border Effect */}
      <div
        className={`absolute -inset-[2px] rounded-lg p-1 transition-all opacity-0 group-hover:opacity-100 group-hover:bg-gradient-to-br ${colorFrom} ${colorTo}`}
      ></div>
      {/* Card Content */}
      <div className="relative flex items-center justify-center w-full h-full bg-white rounded-lg">
        <Image
          src={logo}
          alt={`${name} Logo`}
          className={`group-hover:scale-110 transition-transform ${
            grayscale === "grayscale" ? "grayscale" : ""
          } group-hover:grayscale-0 filter rounded-lg p-2`}
          width={imageWidth}
          height={imageHeight}
        />
      </div>
    </div>
  );
};

export default TechCard;
