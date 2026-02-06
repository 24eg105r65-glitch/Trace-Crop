// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-analytics.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged, GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
import { getFirestore, doc, setDoc, getDoc, collection, addDoc, query, where, getDocs, updateDoc, deleteDoc, limit, orderBy, onSnapshot } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";
import { getStorage, ref, uploadBytes, getDownloadURL } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-storage.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyD-Z6UUa_KzHwf52sp_-l1xIlo6lsrlzoo",
  authDomain: "tracecrop-a756a.firebaseapp.com",
  projectId: "tracecrop-a756a",
  storageBucket: "tracecrop-a756a.firebasestorage.app",
  messagingSenderId: "338713897561",
  appId: "1:338713897561:web:9794ab4f25822af0e11f48",
  measurementId: "G-L48TC2QWH6"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const db = getFirestore(app);
const storage = getStorage(app);
const provider = new GoogleAuthProvider();

export { 
    auth, db, storage, 
    createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged, provider, signInWithPopup,
    doc, setDoc, getDoc, collection, addDoc, query, where, getDocs, updateDoc, deleteDoc, limit, orderBy, onSnapshot,
    ref, uploadBytes, getDownloadURL 
};
