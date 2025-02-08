import { FC, memo } from "react";

import Link from "next/link";

import LogoSvg from "@/public/algotix_logo.svg";
import { clx } from "@/src/utils/helpers";
import Image from "next/image";

interface Props {
  className?: string;
  fill?: string;
}

export const Logo: FC<Props> = memo(({ className }) => {
  return (
    <Link
      href="/"
      aria-label="Algotix AI"
      className={clx("flex items-center", className)}
    >
      <Image src={LogoSvg} alt="Algotix AI Logo" />
    </Link>
  );
});

Logo.displayName = "Logo";
