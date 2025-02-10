import React from "react";

const Contact = () => {
  return (
    <div className="container mx-auto px-6">
      <h1>Contact Us</h1>
      <p>Please feel free to reach out to us at any time.</p>
      <a href="mailto:your@email.com">Email Us</a>
      <p>Phone: (123) 456-7890</p>
      <p>Address: 123 Main St, City, State, ZIP</p>
      <form>
        <input type="text" placeholder="Name" />
        <input type="text" placeholder="Email" />
        <textarea placeholder="Message" rows={4} />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default Contact;
