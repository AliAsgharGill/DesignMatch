export interface ButtonProps {
  type?: "button" | "submit" | "reset";
  width?: string; // Custom width (default 230px)
  height?: string; // Custom height (default 60px)
  variant?: "primary" | "secondary" | "tertiary" | "custom"; // Button variant
  textColor?: string; // Custom text color (default white)
  bgColor?: string; // Custom background color (default orange-600)
  borderColor?: string; // Custom border color (for tertiary)
  fontWeight?: string; // Custom font weight (for tertiary)
  opacity?: number; // Custom opacity
  children: React.ReactNode; // Button text/content
  onClick?: () => void; // Optional onClick handler
  disabled?: boolean; // Optional disabled state
  className?: string; // Additional custom class names for custom styles
  padding?: string; // Custom padding (default px-4 py-2)
  radius?: string; // Custom border radius (default rounded-full)
  shadow?: string; // Custom shadow (default shadow-md)
  shadowColor?: string; // Custom shadow color (default shadow-primary)
  style?: React.CSSProperties; // Optional custom styles
}
