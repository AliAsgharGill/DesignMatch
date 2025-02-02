'use client'

import { useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { usePathname } from 'next/navigation'
import { motion } from 'framer-motion' // Import framer-motion for animations

const Header = () => {
  const [isOpen, setIsOpen] = useState(false)
  const pathname = usePathname() // Get the current route

  const toggleMenu = () => {
    setIsOpen(!isOpen)
  }

  const getLinkClass = (path: string) =>
    pathname === path ? 'text-white font-semibold' : 'text-gray-300'

  return (
    <nav className="px-6 py-4 w-full bg-gradient-to-r from-indigo-600 to-purple-700">
      <div className="flex items-center justify-between container mx-auto">
        {/* Logo */}
        <div className="text-xl font-bold">
          <Link href="/">
            <Image
              src="/images/logo/logo.png"
              alt="Design Match"
              width={120}
              height={40}
            />
          </Link>
        </div>

        {/* Menu on desktop (visible only on large screens) */}
        <div className="hidden lg:flex items-center space-x-6 laptop:space-x-2 desktop:space-x-6">
          <Link href="/design" className={getLinkClass('/design')}>
            Design
          </Link>
          <Link href="/projects" className={getLinkClass('/projects')}>
            Projects
          </Link>
          {/* <Link href="/about" className={getLinkClass("/about")}>
                        About Us
                    </Link>
                    <Link href="/contact" className={getLinkClass("/contact")}>
                        Contact Us
                    </Link>
                    <Link href="/blogs" className={getLinkClass("/blogs")}>
                        Blogs
                    </Link> */}
          {/* <Link
                            href="/faq"
                            className={`pl-6 text-white ${getLinkClass("/faq")}`}
                        >
                            Have Questions?
                        </Link> */}
          {/* <Link
                        href="/consultation"
                        className="bg-indigo-500 text-white px-7 py-3 rounded-full font-semibold transform transition-transform duration-300 hover:scale-105 hover:translate-y-0.5"
                    >
                        Request a Consultation
                    </Link> */}
        </div>

        {/* Hamburger menu for mobile/tablet */}
        <div className="lg:hidden flex items-center">
          <button
            onClick={toggleMenu}
            className="text-white focus:outline-none"
          >
            <motion.svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              strokeWidth="2"
              initial={{ rotate: 0 }}
              animate={{ rotate: isOpen ? 90 : 0 }}
              transition={{ duration: 0.3 }}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M4 6h16M4 12h16M4 18h16"
              ></path>
            </motion.svg>
          </button>
        </div>
      </div>

      {/* Mobile Menu (visible only on small screens, when isOpen is true) */}
      <div
        className={`lg:hidden ${isOpen ? 'block' : 'hidden'} mt-4 space-y-4`}
      >
        <motion.div
          className="space-y-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: isOpen ? 1 : 0 }}
          transition={{ duration: 0.5 }}
        >
          <Link href="/design" className={`block ${getLinkClass('/design')}`}>
            Design
          </Link>
          <Link
            href="/projects"
            className={`block ${getLinkClass('/projects')}`}
          >
            Projects
          </Link>
          {/* <Link href="/about" className={`block ${getLinkClass("/about")}`}>
                        About Us
                    </Link>
                    <Link href="/contact" className={`block ${getLinkClass("/contact")}`}>
                        Contact Us
                    </Link>
                    <Link href="/blogs" className={`block ${getLinkClass("/blogs")}`}>
                        Blogs
                    </Link>
                    <Link href="/faq" className={`block ${getLinkClass("/faq")}`}>
                        Have Questions?
                    </Link>
                    <Link
                        href="/consultation"
                        className="block bg-indigo-500 text-white px-7 py-3 rounded-full font-semibold"
                    >
                        Request a Consultation
                    </Link> */}
        </motion.div>
      </div>
    </nav>
  )
}

export default Header
