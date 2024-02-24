import React from "react";
import main from "./main.css";
import WorkersImage from "../../assets/14.jpg";
import PureComponent from '../LineChart/LineChart'
import CircularProgressBarWithPercentage from "../CircleBar/CircularProgressBar";

const MainPage = () => {
  const percentage = 72;

  return (
    <div className="container">
      {/* header section */}
      <div className="header">
        <div className="imageDiv">
          <img
            src={WorkersImage}
            alt="worker_image"
            className="workerImageStyle"
          />
        </div>
        <div className="personData">
          <h2 className="fullName">МОСЫНОВ ГУСАН ШУХРАТОВИЧ</h2>
          <div className="spaceBetweenDiv">
            <p className="leftText">ФИЛИАЛ /ГО</p>
            <p className="rightText">Главное управление по г.Ташкент</p>
          </div>
          <div className="spaceBetweenDiv">
            <p className="leftText">ВСП (ОПЕРУ/БХМ/БХО)</p>
            <p className="rightText">академическое филиал</p>
          </div>
          <div className="spaceBetweenDiv">
            <p className="leftText">ПОДРАЗДЕЛЕНИЕ</p>
            <p className="rightText">отель обслуживания и выпуска пластиковых карт</p>
          </div>
          <div className="spaceBetweenDiv">
            <p className="leftText">ДОЛЖНОСТЬ</p>
            <p className="rightText">Главный специалист</p>
          </div>
          <div className="spaceBetweenDiv">
            <p className="leftText">ТАБЕЛЬНЫЙ НОМЕР РАБОТНИКА</p>
            <p className="rightText">2552</p>
          </div>
          <div className="spaceBetweenDiv">
            <p className="leftText">ПИНФЛ РОБОТНИКА</p>
            <p className="rightText">32525018332557</p>
          </div>
          <div className="spaceBetweenDiv">
            <p className="leftText">ОКЛАД РАБОТНИКА, СУММ.</p>
            <p className="rightText">1500 000,00</p>
          </div>
        </div>
        <div className="kpiPie">
          <div className="topTexts">
            <h3 className="kpiStyle">KPI</h3>
            <p className="kpiDataText">за июль 2023 г.</p>
          </div>
          <div className="pieCartDiv">
        
            <CircularProgressBarWithPercentage
            selectedValue={percentage}
            maxValue={100}
            radius={140}
            textColor='#000'
            activeStrokeColor='#00ff00'
            withGradient
          />

          </div>
          
        </div>
      </div>
      {/* middle all year information graph */}
      <div className="graphDiv">
      <h4 className="lineChartText">Динамика выполнение общего плановые показателей KPI</h4>
      <PureComponent  className="lineChartStyle" />
      </div>
      <div className="tableMainDiv">
   
    <table>
      <thead>
        <tr className="spaceTable">
          <th className="longest"></th>
          <th><span>ПЛАН</span> </th>
          <th><span>ФАКТ</span></th>
          <th><span>ИСПОЛ %</span></th>
          <th className="stavkaColumn yellowSoul"><span >СТАВКА ПРЕМИРОВАНИЯ, СУМ</span></th>
          <th className="stavkaColumn yellowSoul">СУММА ПРЕМИРОВАНИЯ, СУМ</th>
          {/* Add more column headers as needed */}
        </tr>
      </thead>
      <tbody style={{width:'100%',border:'1px solid red'}}>
          <tr className="firstRow" >
            <td className="leftRounded">Чистая прибл НБУ область/филила/СБу (после нагов)</td>
            <td className="blueTable">500</td>
            <td >487</td>
            <td className="greenTable">97%</td>
            <td>500</td>
            <td className="yellowTable rightRounded">500</td>
            {/* Render more columns based on your data structure */}
          </tr>
          <tr className="firstRow" >
            <td className="leftRounded">Объем кредитного портфеля НБУ,</td>
            <td className="blueTable">1000</td>
            <td >825</td>
            <td className="greenTable">82%</td>
            <td>1000</td>
            <td className="yellowTable rightRounded">1000</td>
            {/* Render more columns based on your data structure */}
          </tr>
          <tr className="firstRow" >
            <td className="leftRounded">ЧПД+ЧНД по региону/филиалу/СБУ</td>
            <td className="blueTable">2500</td>
            <td >2700</td>
            <td className="greenTable">105%</td>
            <td>2500</td>
            <td className="yellowTable rightRounded">2500</td>
            {/* Render more columns based on your data structure */}
          </tr>
          <tr className="firstRow" >
            <td className="leftRounded">Объём кредитов ФЛ за отчётный период</td>
            <td className="blueTable">100</td>
            <td >97</td>
            <td className="greenTable">97%</td>
            <td>11500</td>
            <td className="yellowTable rightRounded">11500</td>
            {/* Render more columns based on your data structure */}
          </tr>
          <tr className="firstRow" >
            <td className="leftRounded">Milliy, QR, Эл. коммерция (универсальный индикатор выполнения плана)</td>
            <td className="blueTable">750</td>
            <td >950</td>
            <td className="greenTable">125%</td>
            <td>750</td>
            <td className="yellowTable rightRounded">750</td>
            {/* Render more columns based on your data structure */}
          </tr>
        
      </tbody>
    </table>


      </div>
     
    </div>
  );
};

export default MainPage;
