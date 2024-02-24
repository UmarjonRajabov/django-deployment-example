import React from "react";
import { useNavigate } from "react-router-dom";

// import login from "./login.css";
import loginStyle from './loginStyle.css'

const Login = () => {

  const navigate = useNavigate();

  const handleLogin = () => {

    navigate("/dashboard")

  }

  return (
    <div className="container">
      <div className="loginContainer">
        <h1 className="welcomeText">Xush kelibsiz</h1>
        <div className="nameInput">
          <input type="text" className="inputSection" placeholder="Name"/>
        </div>
        <div className="nameInput">
          <input type="password" className="inputSection" placeholder="Password"/>
        </div>
        <button className="loginButton" onClick={handleLogin} >Login</button>
        <div className="signDiv">
          <p className="noneText">Don't have an account</p>
          <a href="#" className="signTag">
            <span className="signText">SignUp</span>
          </a>
        </div>
      </div>
    </div>
  );
};

export default Login;
