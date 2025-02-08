"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";

const Header = () => {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname(); // Get the current route

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const getLinkClass = (path: string) =>
    pathname === path ? "text-black font-semibold" : "text-gray-800";

  return (
    <nav className="px-6 py-4 w-full">
      <div className="flex items-center justify-between container mx-auto">
        {/* Logo */}
        <div className="text-xl font-bold">
          <Link href="/">
            <Image
              src="/images/logo/logo.svg"
              alt="AlgotixAI"
              width={120}
              height={40}
            />
          </Link>
        </div>

        {/* Menu on desktop (visible only on large screens) */}
        <div className="hidden lg:flex items-center space-x-6 laptop:space-x-2 desktop:space-x-6">
          <Link href="/services" className={getLinkClass("/services")}>
            Services
          </Link>
          <Link href="/projects" className={getLinkClass("/projects")}>
            Projects
          </Link>
          <Link href="/about" className={getLinkClass("/about")}>
            About Us
          </Link>
          <Link href="/contact" className={getLinkClass("/contact")}>
            Contact Us
          </Link>
          <Link href="/blogs" className={getLinkClass("/blogs")}>
            Blogs
          </Link>
          <Link
            href="/faq"
            className={`pl-6 text-primary ${getLinkClass("/faq")}`}
          >
            Have Questions?
          </Link>
          <Link
            href="/consultation"
            className="bg-primary text-white px-7 py-3 rounded-full font-semibold transform transition-transform duration-300 hover:scale-105 hover:translate-y-0.5"
          >
            Request a Consultation
          </Link>
        </div>

        {/* Hamburger menu for mobile/tablet */}
        <div className="lg:hidden flex items-center">
          <button
            onClick={toggleMenu}
            className="text-gray-600 focus:outline-none"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              strokeWidth="2"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M4 6h16M4 12h16M4 18h16"
              ></path>
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Menu (visible only on small screens, when isOpen is true) */}
      <div
        className={`lg:hidden ${isOpen ? "block" : "hidden"} mt-4 space-y-4`}
      >
        <Link href="/services" className={`block ` + getLinkClass("/services")}>
          Services
        </Link>
        <Link href="/projects" className={`block ` + getLinkClass("/projects")}>
          Projects
        </Link>
        <Link href="/about" className={`block ` + getLinkClass("/about")}>
          About Us
        </Link>
        <Link href="/contact" className={`block ` + getLinkClass("/contact")}>
          Contact Us
        </Link>
        <Link href="/blogs" className={`block ` + getLinkClass("/blogs")}>
          Blogs
        </Link>
        <Link href="/faq" className={`block ` + getLinkClass("/faq")}>
          Have Questions?
        </Link>
        <Link
          href="/consultation"
          className="block bg-primary text-white px-7 py-3 rounded-full font-semibold"
        >
          Request a Consultation
        </Link>
      </div>
    </nav>
  );
};

export default Header;
