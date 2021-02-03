let env;

if (process.env.NODE_ENV !== "production") {  
    env = true;
} else {
    env = false;
}

export const DOMAIN = env ? "http://localhost:8000" : "http://localhost:8000";