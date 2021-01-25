
if (process.env.NODE_ENV !== "production") {  
    env = true;
} else {
    env = false;
}

export const DOMAIN = env ? "http://10.0.0.4:8000" : "http://localhost:8000";