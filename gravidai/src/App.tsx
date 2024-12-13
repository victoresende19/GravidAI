import axios from 'axios';
import React, { useEffect, useState, useRef } from 'react';
import { BsLinkedin, BsGithub } from 'react-icons/bs';
import CircularProgress from '@mui/material/CircularProgress';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import './App.css';

const App: React.FC = () => {
  const [question, setQuestion] = useState('');
  const [chatHistory, setChatHistory] = useState<
    { human: string; ia: string; loading?: boolean }[]
  >([]);
  const [loading, setLoading] = useState(false);
  const [countdown, setCountdown] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuestion(event.target.value);
  };

  const handleSubmit = async () => {
    if (question.trim() === '') return;

    // Adiciona a pergunta ao chat imediatamente com uma resposta vazia e indicador de loading
    const newChatEntry = { human: question, ia: '', loading: true };
    setChatHistory([...chatHistory, newChatEntry]);
    setQuestion('');
    setLoading(true);
    setError(null);

    try {
      const res = await axios.post(
        'https://gravidai-442612.ue.r.appspot.com/ask_question',
        { question }
      );

      const { answer } = res.data;
      console.log(answer)

      // Atualiza a última entrada do chat com a resposta da IA
      setChatHistory((prevChatHistory) => {
        const updatedChatHistory = [...prevChatHistory];
        updatedChatHistory[updatedChatHistory.length - 1] = {
          human: newChatEntry.human,
          ia: answer,
          loading: false,
        };
        return updatedChatHistory;
      });
    } catch (error) {
      setError('Erro ao obter resposta. Tente novamente.');
      // Atualiza o chat com a mensagem de erro
      setChatHistory((prevChatHistory) => {
        const updatedChatHistory = [...prevChatHistory];
        updatedChatHistory[updatedChatHistory.length - 1] = {
          human: newChatEntry.human,
          ia: 'Erro ao obter resposta. Tente novamente.',
          loading: false,
        };
        return updatedChatHistory;
      });
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

  useEffect(() => {
    // Rolagem automática para a última mensagem
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [chatHistory, loading]);

  return (
    <html lang="pt">
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
          }
          .chat-bubble {
            max-width: 70%;
            padding: 10px;
            border-radius: 20px;
            margin-bottom: 1px;
            word-wrap: break-word;
            position: relative;
          }
          .chat-bubble.human {
            background-color: #dcf8c6;
            align-self: flex-end;
            margin-bottom: 20px;
            margin-right: 10px;
          }
          .chat-bubble.ia {
            background-color: #fff;
            align-self: flex-start;
            max-width: 90%;
            margin-bottom: 20px;
          }
          .chat-container {
            display: flex;
            flex-direction: column;
            scroll-behavior: smooth;
          }
          .chat-container::-webkit-scrollbar {
            width: 8px;
          }
          .chat-container::-webkit-scrollbar-track {
            background: #2d3748; /* Cor do track */
            border-radius: 10px;
          }
          .chat-container::-webkit-scrollbar-thumb {
            background: #718096; /* Cor do thumb */
            border-radius: 10px;
          }
          .chat-container::-webkit-scrollbar-thumb:hover {
            background: #4a5568; /* Cor do thumb ao passar o mouse */
          }
          `}
        </style>
      </head>

      <body className="leading-normal tracking-normal text-gray-100 m-6 bg-cover bg-fixed">
        <div className="h-full">
          {/* Cabeçalho */}
          <div className="w-full container mx-auto">
            <div className="w-full flex items-center justify-between">
              <a
                className="flex items-center text-white no-underline hover:no-underline font-bold text-2xl lg:text-4xl"
                href="#"
              >
                Gravid
                <span className="bg-clip-text text-transparent bg-gradient-to-r text-pink-200 ">
                  AI
                </span>
              </a>
              <div className="flex w-1/2 justify-end content-center">
                <a
                  className="inline-block text-white-300 no-underline hover:text-pink-500 hover:text-underline text-right h-10 p-2 md:h-auto md:p-4 transform hover:scale-125 duration-300 ease-in-out"
                >
                  Acesse as redes sociais
                </a>
                <a
                  className="inline-block text-white-300 no-underline hover:text-pink-500 hover:text-underline text-right h-10 p-2 md:h-auto md:p-4 transform hover:scale-125 duration-300 ease-in-out"
                  href="https://github.com/victoresende19"
                  target="_blank"
                >
                  <BsGithub />
                </a>
                <a
                  className="inline-block text-white-300 no-underline hover:text-pink-500 hover:text-underline text-right h-10 p-2 md:h-auto md:p-4 transform hover:scale-125 duration-300 ease-in-out"
                  href="https://www.linkedin.com/in/victor-resende-508b75196/"
                  target="_blank"
                >
                  <BsLinkedin />
                </a>
              </div>
            </div>
          </div>

          {/* Conteúdo principal */}
          <div className="container pt-5 md:pt-15 mx-auto flex flex-col items-center justify-center text-center">
            {/* Informações do site */}
            <div className="w-full lg:w-2/3 flex flex-col items-start p-2">
              <p className="text-4xl font-bold text-white mb-1">
                Cuidando de você e do seu bebê com tecnologia e carinho
                <br />
                <br />
              </p>
              <p className="text-lg text-white mb-4 text-justify">
                O que o GravidAI faz?<br />
                <ul className="list-disc list-inside text-lg text-white mb-4">
                  <li>Responde suas dúvidas: Seja sobre alimentação, cuidados, exames ou sintomas de você e seu bebê. O GravidAI está aqui para te ajudar.</li>
                  <li>Oferece informações confiáveis: As respostas vêm de guias médicos e dados atualizados, feitos para te tranquilizar.</li>
                  <li>Está sempre disponível: 24 horas por dia, 7 dias por semana, pronto para ajudar quando você precisar.</li>
                </ul>
              </p>
              <p className="text-sm text-white">
                Nunca deixe de validar as informações com seu respectivo médico
              </p>
            </div>

            {/* Chat abaixo das informações */}
            {/* Chat abaixo das informações */}
            <div className="w-full md:w-3/4 lg:w-2/3 flex flex-col items-center p-1">
              <div
                className="w-full opacity-75 shadow-lg rounded-lg px-5 pt-5 pb-8 mb-1"
                style={{
                  height: '500px',
                  display: 'flex',
                  flexDirection: 'column',
                  backgroundColor: '#4d2f35'
                }}
              >
                <div
                  className="chat-container flex-1 mb-4"
                  style={{
                    minHeight: '300px',
                    maxHeight: '400px',
                    overflowY: 'auto',
                  }}
                  ref={chatContainerRef}
                >
                  {chatHistory.length === 0 ? (
                    <div className="text-center text-gray-400 mt-10 text-xl">
                      Nenhuma interação ainda. Faça uma pergunta sobre cuidados de você e seu bebê!
                    </div>
                  ) : (
                    chatHistory.map((message, index) => (
                      <React.Fragment key={index}>
                        <div className="chat-bubble human self-end">
                          <p className="text-black">{message.human}</p>
                        </div>
                        <div className="chat-bubble ia">
                          {message.loading ? (
                            <Box
                              sx={{
                                display: 'flex',
                                justifyContent: 'center',
                                alignItems: 'center',
                                minHeight: '20px',
                              }}
                            >
                              <CircularProgress size={20} />
                            </Box>
                          ) : (
                            <p className="text-black">{message.ia}</p>
                          )}
                        </div>
                      </React.Fragment>
                    ))
                  )}
                </div>
                <form
                  className="flex"
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleSubmit();
                  }}
                >
                  <TextField
                    id="outlined-multiline-flexible"
                    value={question}
                    onChange={handleInputChange}
                    multiline
                    rows={2}
                    placeholder="Digite sua pergunta..."
                    className="flex-grow shadow appearance-none border rounded w-full py-2 px-3 text-black bg-white leading-tight focus:outline-none focus:shadow-outline"
                  />
                  <button
                    className="ml-2 bg-gradient-to-r from-pink-500 to-pink-900 text-slate-50 font-bold py-2 px-4 rounded focus:ring transform transition hover:scale-105 duration-300 ease-in-out"
                    type="submit"
                    disabled={loading}
                  >
                    Enviar
                  </button>
                </form>
                {error && <div className="text-red-500 mt-2">{error}</div>}
              </div>
            </div>
          </div>

          {/* Rodapé */}
          <div className="w-full pt-1 pb-6 text-sm text-center fade-in">
            <a className="text-white-500 no-underline hover:no-underline" href="#">
              &copy; 2024{' '}
            </a>
            - Victor Augusto Souza Resende
          </div>
        </div>
      </body>
    </html>
  );
};

export default App;