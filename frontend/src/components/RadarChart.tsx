import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';

export default function ResultsChart({ innovation, architecture, impact}: {
  innovation: number; 
  architecture: number; 
  impact: number;
}) {

const data = [
  { subject: 'Innovation', A: innovation * 10, fullMark: 100 },
  { subject: 'Architecture', A: architecture * 10, fullMark: 100 },
  { subject: 'Impact', A: impact * 10, fullMark: 100 },
  // { subject: 'Code Quality', A: 80, fullMark: 100 },
  // { subject: 'Security', A: 75, fullMark: 100 },
];

// export default function ResultsChart() {
  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
          <PolarGrid stroke="#374151" />
          <PolarAngleAxis dataKey="subject" stroke="#9CA3AF" />
          <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#374151" />
          <Radar name="Repo" dataKey="A" stroke="#ef4444" fill="#ef4444" fillOpacity={0.6} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}