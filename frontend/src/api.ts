import { io, Socket } from "socket.io-client";

const WEBSOCKET_URL = process.env.REACT_APP_WEBSOCKET_URL || "http://localhost:8000";

let socket: Socket;

export const getSocket = (): Socket => {
  if (!socket) {
    socket = io(WEBSOCKET_URL, {
      transports: ["websocket"],
      path: "/socket.io",
    });

    socket.on("connect", () => console.log(`Socket connected: ${socket.id}`));
    socket.on("disconnect", () => console.log("Socket disconnected"));
  }
  return socket;
};

export const placeBet = (bet: {
  second: number;
  amount: number;
  power_up?: string;
}) => {
  return new Promise((resolve, reject) => {
    const sock = getSocket();
    if (!sock.connected) return reject("Socket not connected");

    sock.emit("place_bet", bet, (response: any) => {
      if (response.status === "success") {
        resolve(response);
      } else {
        reject(response.message);
      }
    });
  });
};