---
name: eng-state-management
description: "Choose and implement state management patterns for frontend and backend applications. Use when designing data flow, global state, or synchronizing client-server state."
---

# State Management for Prototypes

Keep state organized and predictable. At 1000 users, start simple and only add complexity when you have a real problem.

## Frontend State

### Start Here: React Context + useState/useReducer

Sufficient for most prototypes. Don't reach for Redux until you have:
- 5+ components needing the same state
- Complex state updates with multiple actions
- Need for time-travel debugging or middleware

```javascript
// Simple global state with Context
const UserContext = createContext();

function UserProvider({ children }) {
  const [user, setUser] = useState(null);
  
  const login = async (credentials) => {
    const user = await api.login(credentials);
    setUser(user);
    localStorage.setItem('token', user.token);
  };
  
  return (
    <UserContext.Provider value={{ user, login }}>
      {children}
    </UserContext.Provider>
  );
}
```

### When to Upgrade

| State Complexity | Solution |
|------------------|----------|
| 1–2 shared values | `useState` + prop drilling |
| 3–5 shared values | React Context |
| 5+ values, async actions | Zustand, Jotai, or Valtio |
| Complex domain logic | Redux Toolkit, Zustand |
| Server state (caching, sync) | TanStack Query (React Query), SWR |

### Server State: TanStack Query

```javascript
// Automatically caches, invalidates, and syncs server state
const { data: posts, isLoading } = useQuery({
  queryKey: ['posts'],
  queryFn: fetchPosts,
  staleTime: 5 * 60 * 1000, // 5 minutes
});

const mutation = useMutation({
  mutationFn: createPost,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['posts'] });
  }
});
```

**Why TanStack Query:**
- Eliminates manual cache management
- Handles loading/error states automatically
- Background refetching
- Optimistic updates

## Backend State

### Session State

```javascript
// Server-side session with Redis
app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: { secure: true, httpOnly: true, maxAge: 86400000 }
}));
```

### Application State (In-Memory)

```javascript
// Simple in-memory state for non-persistent data
const appState = {
  activeConnections: new Map(),
  rateLimitCounters: new Map(),
  featureFlags: new Map()
};

// For multi-instance deployments, move to Redis
```

## State Design Principles

### 1. Normalize State Shape

```javascript
// ❌ Nested arrays — hard to update
const state = {
  posts: [
    { id: 1, title: 'Hello', author: { id: 1, name: 'Alice' } }
  ]
};

// ✅ Flat, normalized — easy to update
const state = {
  posts: {
    byId: { 1: { id: 1, title: 'Hello', authorId: 1 } },
    allIds: [1]
  },
  users: {
    byId: { 1: { id: 1, name: 'Alice' } },
    allIds: [1]
  }
};
```

### 2. Single Source of Truth

- Server state = database (source of truth)
- Client state = UI-specific (filters, modals, forms)
- Don't duplicate server state in client state — cache it

### 3. Immutable Updates

```javascript
// Always return new objects/arrays
setUser({ ...user, name: 'New Name' });
setPosts(posts.map(p => p.id === id ? { ...p, title: newTitle } : p));
```

### 4. State Colocation

Keep state as close to where it's used as possible:
- Component-local state → `useState`
- Shared component state → Context
- Global app state → State management library
- Server state → TanStack Query / SWR

## URL as State

For shareable/filterable views, encode state in the URL:

```javascript
// /products?category=shoes&sort=price&page=2
const [searchParams, setSearchParams] = useSearchParams();

const category = searchParams.get('category');
const setCategory = (cat) => setSearchParams({ category: cat });
```

**Benefits:** Shareable links, browser back/forward works, no state sync needed.

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| Put everything in global state | Colocate state where it's used |
| Duplicate server state in Redux | Use TanStack Query for server state |
| Use Redux for simple apps | Start with Context, upgrade when needed |
| Mutate state directly | Always create new objects/arrays |
| Store derived state | Compute on render with `useMemo` |
| Mix UI state and domain state | Separate concerns |
| Ignore state hydration (SSR) | Handle rehydration explicitly |
