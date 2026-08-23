import { createContext, useContext, type PropsWithChildren } from "react";

// [Implementation 0]
// Route UI가 먼저 조립될 수 있도록 application boundary만 제공합니다.
export type FieldNotesContextValue = { ready: boolean };

const FieldNotesContext = createContext<FieldNotesContextValue>({ ready: false });

export function FieldNotesProvider({ children }: PropsWithChildren) {
  return (
    <FieldNotesContext.Provider value={{ ready: false }}>
      {children}
    </FieldNotesContext.Provider>
  );
}

export function useFieldNotes(): FieldNotesContextValue {
  return useContext(FieldNotesContext);
}
