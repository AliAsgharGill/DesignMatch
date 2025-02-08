import Carousel from "@/src/components/carousel/carousel";
import Hero from "@/src/components/hero";
import { workWithUsData } from "@/src/components/home/data";
import WorkWithUsSection from "@/src/components/home/work-with-us";

export default function Home() {
  return (
    <div className="">
      <div className="container mx-auto px-6 w-full">
        <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start w-full">
          <div className="flex flex-col items-center justify-center w-full h-full">
            <Hero />
          </div>
        </main>
      </div>
      {/* <div className="absolute bg-custom-svg bg-cover -mt-10 w-full h-full" /> */}
      <Carousel />
      <WorkWithUsSection data={workWithUsData} />
    </div>
  );
}
