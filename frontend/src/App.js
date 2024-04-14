import "./App.css";
import { useRef, useState } from "react";

function App() {
  const ref = useRef(null);
  const [data, setdata] = useState([]);
  const submitvalue = async (e) => {
    e.preventDefault();
    const value = ref.current.value;
    const res = await fetch(`http://localhost:8000/${value}`);
    const json = await res.json();
    setdata(json);
  };
  return (
    <div className="w-screen h-screen bg-gray-500 flex flex-col items-center">
      <h1 className="mt-6 text-3xl">好きなチャンネルのIDを入力しましょう</h1>
      <form className="flex flex-col items-center">
        <input ref={ref} type="text" />
        <button
          onClick={(e) => {
            submitvalue(e);
          }}
        >
          送信
        </button>
      </form>

      <div id="box" className="w-[600px] mt-5 flex flex-col items-center">
        {data
          ? data.map((value) => {
              return (
                <div className="w-full h-[99px]  flex flex-col border-x-2 border-t-2 border-black ">
                  <p className="text-center h-[33px]">タイトル:　{value[0]}</p>
                  <p className="text-center h-[33px]">再生数:　{value[1]}</p>
                  <p className="text-center h-[33px]">
                    url:　{`https://www.youtube.com/watch?v=${value[2]}`}
                  </p>
                </div>
              );
            })
          : null}
      </div>
    </div>
  );
}

export default App;
