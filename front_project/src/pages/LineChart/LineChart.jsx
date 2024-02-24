import React, { PureComponent } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ReferenceLine,
  ResponsiveContainer,
} from 'recharts';

const data = [
  {
    name: 'февраль 2022',
    uv: 97,
    pv: 97, // hover value
    amt: "97%",
  },
  {
    name: 'март 2022',
    uv: 90,
    pv: 90,
    amt: 90,
  },
  {
    name: 'апрель 2022',
    uv: 92,
    pv: 92,
    amt: 92,
  },
  {
    name: 'май 2022',
    uv: 100,
    pv: 100,
    amt: 100,
  },
  {
    name: 'май 2022',
    uv: 100,
    pv: 100,
    amt: 100,
  },
  {
    name: 'апрель 2022',
    uv: 92,
    pv: 92,
    amt: 92,
  },
  {
    name: 'март 2022',
    uv: 90,
    pv: 90,
    amt: 90,
  },
  {
    name: 'февраль 2022',
    uv: 97,
    pv: 97, // hover value
    amt: "97%",
  },
  {
    name: 'февраль 2022',
    uv: 97,
    pv: 97, // hover value
    amt: "97%",
  },
  {
    name: 'февраль 2022',
    uv: 75,
    pv: 75, // hover value
    amt: "75%",
  },
  {
    name: 'февраль 2022',
    uv: 97,
    pv: 97, // hover value
    amt: "97%",
  },
  {
    name: 'февраль 2022',
    uv: 97,
    pv: 97, // hover value
    amt: "97%",
  },
  {
    name: 'февраль 2022',
    uv: 97,
    pv: 97, // hover value
    amt: "97%",
  },
  {
    name: 'апрель 2022',
    uv: 110,
    pv: 110,
    amt: 110,
  },
  {
    name: 'апрель 2022',
    uv: 92,
    pv: 92,
    amt: 92,
  },
  {
    name: 'апрель 2022',
    uv: 60,
    pv: 60,
    amt: 60,
  },
  {
    name: 'апрель 2023',
    uv: 92,
    pv: 92,
    amt: 92,
  },

];

export default class Example extends PureComponent {
  static demoUrl = 'https://codesandbox.io/s/line-chart-width-xaxis-padding-sujqi';

  render() {
    return (
      <ResponsiveContainer width="100%" height="100%">
        <LineChart width={500} height={300} data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" padding={{ left: 30, right: 30 ,}} />
          <YAxis tickFormatter={(value) => `${value}%`} domain={[60, 120]} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="pv" stroke="#00ff00" activeDot={{ r:8 }} />
        </LineChart>
      </ResponsiveContainer>
    );
  }
}