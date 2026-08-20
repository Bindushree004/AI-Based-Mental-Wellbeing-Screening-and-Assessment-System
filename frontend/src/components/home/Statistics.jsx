import "../../styles/Statistics.css";

import {
  FaBrain,
  FaHeart,
  FaGlobe,
} from "react-icons/fa";

function Statistics() {

  const cards = [

    {
      icon: <FaBrain />,
      title: "Early Awareness",
      description:
        "Recognizing emotional changes early helps individuals seek support before problems become more serious.",
    },

    {
      icon: <FaHeart />,
      title: "Healthy Lifestyle",
      description:
        "Understanding your mental wellbeing encourages healthier habits, emotional balance, and self-care.",
    },

    {
      icon: <FaGlobe />,
      title: "Better Quality of Life",
      description:
        "Good mental wellbeing improves relationships, academic performance, work productivity, and daily living.",
    },

  ];

  return (

    <section className="statistics">

      <h2>Why Mental Wellbeing Matters</h2>

      <p className="statistics-subtitle">
        Mental wellbeing plays an essential role in living a balanced,
        productive, and fulfilling life.
      </p>

      <div className="statistics-grid">

        {cards.map((card, index) => (

          <div className="statistics-card" key={index}>

            <div className="statistics-icon">
              {card.icon}
            </div>

            <h3>{card.title}</h3>

            <p>{card.description}</p>

          </div>

        ))}

      </div>

    </section>

  );

}

export default Statistics;