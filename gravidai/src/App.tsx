import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { BsLinkedin, BsGithub } from 'react-icons/bs';
import { MdPregnantWoman } from "react-icons/md";
import { RiRobot3Fill } from "react-icons/ri";
import CircularProgress from '@mui/material/CircularProgress';
import TextField from '@mui/material/TextField';
import './App.css';

interface HistoryEntry {
  human: string;
  ia: string;
}

interface ApiResponse {
  question: string;
  answer: string;
  history: HistoryEntry[];
}

const App: React.FC = () => {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [countdown, setCountdown] = useState(20);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuestion(event.target.value);
  };

  const handleSubmit = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setError(null);

    const currentQuestion = question; 

    setResponse((prev) => {
      const updatedHistory = prev?.history ? [...prev.history] : [];

      if (!updatedHistory.length || updatedHistory[updatedHistory.length - 1].ia !== '...') {
        updatedHistory.push({ human: currentQuestion, ia: '...' });
      }

      return {
        ...(prev || { question: '', answer: '' }),
        history: updatedHistory
      };
    });

    setQuestion('');

    try {
      const res = await axios.post('https://gravidai.onrender.com/ask_question', { question: currentQuestion });
      setResponse((prev) => {
        const updatedHistory = prev?.history
          ? prev.history.filter(entry => entry.ia !== '...')
          : [];

        updatedHistory.push({ human: currentQuestion, ia: res.data.answer });

        return {
          ...res.data,
          history: updatedHistory
        };
      });
    } catch (error) {
      setError('Erro ao obter resposta. Tente novamente.');

      setResponse((prev) => ({
        ...(prev || { question: '', answer: '' }),
        history: prev?.history ? prev.history.filter(entry => entry.ia !== '...') : []
      }));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (loading && countdown > 0) {
      timer = setInterval(() => {
        setCountdown((prevCountdown) => prevCountdown - 1);
      }, 1000);
    } else if (countdown === 0) {
      setLoading(false);
    }

    return () => clearInterval(timer);
  }, [loading, countdown]);

  return (
    <html lang="en">
      <head>
        <link
          rel="stylesheet"
          href="https://unpkg.com/tailwindcss@2.2.19/dist/tailwind.min.css"
        />
        <link
          href="https://unpkg.com/@tailwindcss/custom-forms/dist/custom-forms.min.css"
          rel="stylesheet"
        />
        <style>
          {`@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap");
          html {
            font-family: "Poppins", -apple-system,
              BlinkMacSystemFont, "Segoe UI", Roboto,
              "Helvetica Neue", Arial, "Noto Sans",
              sans-serif, "Apple Color Emoji",
              "Segoe UI Emoji", "Segoe UI Symbol",
              "Noto Color Emoji";
          }`}
        </style>
      </head>
      
      {/* Header */}
      <body className="leading-normal tracking-normal text-gray-100 m-6 bg-cover bg-fixed">
        <div className="h-full">
          <div className="w-full container mx-auto">
            <div className="w-full flex items-center justify-between">
              <a
                className="flex items-center text-white no-underline hover:no-underline font-bold text-2xl lg:text-4xl"
                href="#"
              >
                Gravid
                <span
                  className="bg-clip-text text-transparent bg-gradient-to-r"
                  style={{ backgroundColor: '#F8C6C6' }}
                >
                  AI
                </span>
              </a>
              <div className="flex w-1/2 justify-end content-center">
                <a
                  className="inline-block text-blue-300 no-underline hover:text-pink-500 hover:text-underline text-right h-10 p-2 md:h-auto md:p-4 transform hover:scale-125 duration-300 ease-in-out"
                  style={{ color: '#6D4B51' }}
                >
                  Acesse as redes sociais
                </a>
                <a
                  className="inline-block no-underline hover:text-pink-500 hover:text-underline text-right h-10 p-2 md:h-auto md:p-4 transform hover:scale-125 duration-300 ease-in-out"
                  href="https://github.com/victoresende19"
                  target="_blank"
                  style={{ color: '#6D4B51' }}
                >
                  <BsGithub />
                </a>
                <a
                  className="inline-block no-underline hover:text-pink-500 hover:text-underline text-right h-10 p-2 md:h-auto md:p-4 transform hover:scale-125 duration-300 ease-in-out"
                  href="https://www.linkedin.com/in/victor-resende-508b75196/"
                  target="_blank"
                  style={{ color: '#6D4B51' }}
                >
                  <BsLinkedin />
                </a>
              </div>
            </div>
          </div>

          {/* Informacoes */}
          <div className="container pt-24 md:pt-100 mx-auto flex flex-wrap flex-col md:flex-row items-center justify-center text-center">
            <p className="text-4xl font-bold text-white mb-6">
              Cuidando de você e do seu bebê com tecnologia e carinho
              <br />
              <br />
            </p>
            <p className="text-lg text-white mb-4 text-justify">
              O que o GravidAI faz?<br />
              <ul className="list-disc list-inside text-lg text-white mb-4">
                <li>Responde suas dúvidas: Seja sobre alimentação, cuidados, exames ou sintomas, o GravidAI está aqui para te ajudar.</li>
                <li>Oferece informações confiáveis: As respostas vêm de guias médicos e dados atualizados, feitos para te tranquilizar.</li>
                <li>Está sempre disponível: 24 horas por dia, 7 dias por semana, pronto para ajudar quando você precisar.</li>
              </ul>
            </p>
            <p className="text-sm text-white justify-start">
              <br />
              Nunca deixe de validar as informações com seu respectivo médico.
            </p>

            {/* Chat */}
            <div className="container pt-10 md:pt-10 mx-auto flex flex-col items-center lg:px-20 xl:px-40">
              <div className="w-full overflow-hidden relative flex flex-col items-center">
                <div
                  className="opacity-75 w-full shadow-lg rounded-lg px-4 md:px-8 pt-6 pb-8 mb-4"
                  style={{ backgroundColor: '#4d2f35' }}
                >
                  <p className="text-2xl text-white font-bold mb-4">Conversa</p>
                  <div
                    className="flex flex-col gap-4 h-[70vh] max-h-[600px] overflow-y-auto p-4 rounded-md"
                    style={{ backgroundColor: '#3b282b' }}
                  >
                    {response?.history?.map((entry, index) => (
                      <div key={index} className="flex flex-col gap-3 w-full">
                        <div className="flex items-start gap-3 w-full">
                          <div className="flex items-center justify-center min-w-[40px] min-h-[40px] sm:min-w-[50px] sm:min-h-[50px] md:min-w-[60px] md:min-h-[60px] rounded-full bg-white/20">
                            <MdPregnantWoman className="w-6 h-6 sm:w-8 sm:h-8 md:w-10 md:h-10 text-white" />
                          </div>
                          <div
                            className="flex flex-col p-3 rounded-md w-[60%]"
                            style={{ backgroundColor: '#94626a' }}
                          >
                            <p className="text-white break-words text-justify whitespace-pre-wrap">
                              {entry.human}
                            </p>
                          </div>
                        </div>
                        <div className="flex items-start gap-3 w-full self-end">
                          <div
                            className="flex flex-col p-3 rounded-md w-[60%] ml-auto"
                            style={{ backgroundColor: '#6b4c52' }}
                          >
                            <p className="text-white break-words text-justify whitespace-pre-wrap">
                              {entry.ia}
                            </p>
                          </div>
                          <div className="flex items-center justify-center min-w-[40px] min-h-[40px] sm:min-w-[50px] sm:min-h-[50px] md:min-w-[60px] md:min-h-[60px] rounded-full bg-white/20">
                            <RiRobot3Fill className="w-6 h-6 sm:w-8 sm:h-8 md:w-10 md:h-10 text-white" />
                          </div>
                        </div>
                      </div>
                    ))}

                    {!response?.history?.length && (
                      <p className="text-white text-center">
                        Nenhuma interação ainda. Faça uma pergunta e tire suas dúvidas sobre sua gestação!
                      </p>
                    )}
                  </div>

                  <div className="mb-4 mt-4">
                    <div className="relative">
                      {loading ? (
                        <div className="flex items-center justify-center gap-2">
                          <CircularProgress color="inherit" size={30} />
                          <span className="text-white">Gerando resposta...</span>
                        </div>
                      ) : (
                        <TextField
                          fullWidth
                          id="outlined-multiline-flexible"
                          value={question}
                          onChange={handleInputChange}
                          multiline
                          rows={3}
                          placeholder="Faça uma pergunta relacionado à gestação..."
                          className="bg-white rounded"
                          variant="outlined"
                        />
                      )}
                    </div>
                    <div className="flex items-center pt-4 justify-end">
                      {!loading && (
                        <button
                          className="bg-gradient-to-r from-pink-600 to-pink-900 text-slate-50 font-bold py-2 px-4 rounded focus:ring transform transition hover:scale-105 duration-300 ease-in-out"
                          type="button"
                          onClick={handleSubmit}
                        >
                          Perguntar
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Footer */}
            <div className="w-full pt-16 pb-6 text-sm text-center md:text-left fade-in">
              <a className="text-white-500 no-underline hover:no-underline" href="#">&copy; 2024 </a>
              - Victor Augusto Souza Resende
            </div>
          </div>
        </div>
      </body>
    </html>
  );
};

export default App;
