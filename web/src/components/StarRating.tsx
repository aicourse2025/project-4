interface StarRatingProps {
    rating: number
}

export default function StarRating({ rating = 0 }: StarRatingProps) {
    const fullStars = Math.floor(rating);
    const emptyStars = 5 - fullStars
  
    return (
      <div className="text-yellow-500 text-lg">
        {"★".repeat(fullStars)}
        {"☆".repeat(emptyStars)}
      </div>
    );
  }
  