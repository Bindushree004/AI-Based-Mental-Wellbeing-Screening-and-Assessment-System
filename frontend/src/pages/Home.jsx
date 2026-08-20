import Hero from "../components/home/Hero";
import Features from "../components/home/Features";
import HowItWorks from "../components/home/HowItWorks";
import Statistics from "../components/home/Statistics";
import FAQ from "../components/home/FAQ";
import CallToAction from "../components/home/CallToAction";

function Home() {
  return (
    <>
      <Hero />
      <Features />
      <HowItWorks />
      <Statistics />
      <FAQ />
      <CallToAction />
    </>
  );
}

export default Home;