import { useState } from "react";
import "../../styles/FAQ.css";
import { FaChevronDown, FaChevronUp } from "react-icons/fa";

function FAQ() {
  const faqs = [
    {
      question: "Is my data secure?",
      answer:
        "Yes. Your assessment data is securely stored and protected. Only authorized users can access their own information.",
    },
    {
      question: "Is this a medical diagnosis?",
      answer:
        "No. MindSync AI is a mental wellbeing screening tool designed to provide insights. It should not replace professional medical advice.",
    },
    {
      question: "How long does the assessment take?",
      answer:
        "The assessment usually takes between 5 and 10 minutes to complete.",
    },
    {
      question: "Can I view my previous assessments?",
      answer:
        "Yes. All completed assessments will be available in your dashboard history.",
    },
  ];

  const [openIndex, setOpenIndex] = useState(null);

  const toggleFAQ = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <section className="faq-section">
      <h2>Frequently Asked Questions</h2>

      <p className="faq-subtitle">
        Find answers to common questions about MindSync AI.
      </p>

      <div className="faq-container">
        {faqs.map((faq, index) => (
          <div className="faq-item" key={index}>
            <div
              className="faq-question"
              onClick={() => toggleFAQ(index)}
            >
              <h3>{faq.question}</h3>

              {openIndex === index ? (
                <FaChevronUp />
              ) : (
                <FaChevronDown />
              )}
            </div>

            {openIndex === index && (
              <p className="faq-answer">{faq.answer}</p>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}

export default FAQ;