const Spinner = ({ position = "left", size = 20, color = "white" }) => {
  const alignmentClass = {
    left: "justify-start",
    right: "justify-end",
    center: "justify-center",
  }[position];

  // Inline styles to customize size and color
  const spinnerStyle = {
    width: `${size}px`,
    height: `${size}px`,
    borderWidth: `${size / 8}px`, // Set border width relative to the size
    borderColor: color, // Set the color of the spinner
    borderBottomColor: "transparent", // Keep the bottom part transparent to create the spinning effect
  };

  return (
    <span
      className={`absolute inset-0 flex items-center px-5 ${alignmentClass}`}
    >
      <span className="rounded-full animate-spinner" style={spinnerStyle} />
    </span>
  );
};

export default Spinner;
