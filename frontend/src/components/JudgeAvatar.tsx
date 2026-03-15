interface Props {
  name: string;
  avatarColor: string;
}

export default function JudgeAvatar({ name, avatarColor }: Props) {
  // A simple colored circle with the first letter of the judge's name
  return (
    <div className={`w-10 h-10 rounded-full ${avatarColor} flex items-center justify-center font-bold text-white shadow-lg`}>
      {name[0]}
    </div>
  );
}