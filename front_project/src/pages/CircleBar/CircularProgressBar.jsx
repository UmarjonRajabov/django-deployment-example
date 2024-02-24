import React from "react";
import { CircularProgressbarWithChildren } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";

const CircularProgressBarWithPercentage = ({
  selectedValue,
  maxValue,
  radius,
  textColor,
  activeStrokeColor,
  withGradient,
}) => {
  const formattedValue = selectedValue + "%";

  return (
    <div style={{ width: "140px", marginTop: "15px" }}>
      <CircularProgressbarWithChildren
        value={selectedValue}
        maxValue={maxValue}
        strokeWidth={8}
        styles={{
          path: {
            stroke: activeStrokeColor,
            strokeLinecap: "round",
            transition: "stroke-dashoffset 0.5s ease 0s",
          },
          root: {
            width: "140px",
            marginTop: "15px",
           
          },
          trail: {
            stroke: "#f2f2f2",
          },
          text: {
            fill: textColor,
            fontSize: "18px",
            fontWeight: "800",
            dominantBaseline: "central",
            textAnchor: "middle",
          },
        }}
      >
        <div style={{ fontSize: "18px", fontWeight: "800" }}>
          {formattedValue}
        </div>
      </CircularProgressbarWithChildren>
    </div>
  );
};

export default CircularProgressBarWithPercentage;