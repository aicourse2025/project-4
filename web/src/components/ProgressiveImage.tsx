import { useState } from "react";

interface ProgressiveImageProps {
    imageURLs: string[]
    placeholder: string
}

function ProgressiveImage({ imageURLs = [], placeholder = "/images/placeholder.png" }: ProgressiveImageProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [errorCount, setErrorCount] = useState(0);

  if (!imageURLs || imageURLs.length === 0) {
    return <img       className="w-32 h-32 object-cover rounded-md mb-3"
    src={placeholder}/>;
  }

  const handleError = () => {
    const nextIndex = currentIndex + 1;
    if (nextIndex < imageURLs.length) {
      setCurrentIndex(nextIndex);
      setErrorCount(errorCount + 1);
    } else {
      setErrorCount(errorCount + 1);
    }
  };

  if (errorCount >= imageURLs.length) {
    return <img       
    className="w-32 h-32 object-cover rounded-md mb-3"
    src={placeholder}  />;
  }

  return (
    <img
      className="w-32 h-32 object-cover rounded-md mb-3"
      src={imageURLs[currentIndex]}
      onError={handleError}
    />
  );
}

export default ProgressiveImage;
