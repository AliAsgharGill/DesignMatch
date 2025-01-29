import Link from "next/link";

const NotFound = () => {
  return (
    <div className="flex items-center justify-center min-h-[90vh] px-6">
      <div className="text-center max-w-md">
        <h1 className="text-5xl font-extrabold text-gray-800 mb-6">
          404 - Page Not Found
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Sorry, the page you are looking for doesn&apos;t exist. You may have
          mistyped the address or the page may have moved.
        </p>
        <Link
          href="/"
          className="inline-block bg-primary text-white text-lg font-medium py-3 px-6 rounded-lg shadow-md hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2"
        >
          Go Back to Home
        </Link>
      </div>
    </div>
  );
};

export default NotFound;
