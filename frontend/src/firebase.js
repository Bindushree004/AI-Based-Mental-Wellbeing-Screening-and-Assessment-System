import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCPmUwxjBBu6mL3OdqGRDsrRJb-NYneloI",
  authDomain: "mindsync-ai-3cd7a.firebaseapp.com",
  projectId: "mindsync-ai-3cd7a",
  storageBucket: "mindsync-ai-3cd7a.firebasestorage.app",
  messagingSenderId: "994285584353",
  appId: "1:994285584353:web:decfe68fc99f0e7e791ca0"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);

export default app;