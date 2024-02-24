import './App.css';
import {BrowserRouter,Routes,Route} from 'react-router-dom'
import SignUp from './pages/SignUp/SignUp';
import Login from './pages/login/Login';
import MainPage from './pages/Main/MainPage';

function App() {
  return <BrowserRouter>
    <Routes>
     <Route exact path='/' element={<Login/>} />
     <Route exact path='/dashboard' element={<MainPage/>} />
     <Route exact path='/signup' element={<SignUp/>} />
    </Routes>
  </BrowserRouter>
}

export default App;
