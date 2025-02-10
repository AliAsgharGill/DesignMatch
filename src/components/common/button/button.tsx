import React from "react";
import { ButtonProps } from "./types";

const Button: React.FC<ButtonProps> = ({
  type = "button",
  width = "230px",
  height = "40px",
  variant = "primary",
  textColor = "text-primary",
  bgColor = "bg-primary",
  borderColor = "border-primary",
  fontWeight = "font-normal",
  opacity = 1,
  padding = "px-5 py-3",
  radius = "rounded-full",
  children,
  onClick,
  disabled = false,
  className = "",
  shadow = "shadow-md",
  shadowColor = "shadow-primaryLight",
  style,
}) => {
  const baseStyles = `${textColor} ${padding} ${fontWeight} w-[${width}] h-[${height}] ${radius} flex justify-center items-center gap-0 transition-all duration-300 ease-out opacity-${opacity} ${disabled ? "cursor-not-allowed opacity-50" : ""} ${className}`;

  const variantStyles = {
    primary: `${baseStyles} ${bgColor}  shadow-md text-white bg-[linear-gradient(315deg,_#FF5A01_0%,_#FD5901_100%)] hover:bg-primary-dark`,
    secondary: `${baseStyles} bg-white text-primary shadow-md hover:bg-primary-light`,
    tertiary: `${baseStyles} border-2 ${borderColor} ${shadow} hover:${shadowColor} hover:shadow-md text-primary hover:bg-primary-light border-opacity-50 rounded-full`,
    custom: `${className} ${shadow} hover:${shadowColor} rounded-full`,
  };

  return (
    <button
      className={variantStyles[variant]}
      onClick={!disabled ? onClick : undefined}
      disabled={disabled}
      type={type}
      style={style}
    >
      {children}
    </button>
  );
};

export default Button;
