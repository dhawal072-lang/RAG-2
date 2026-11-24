
"use client";

import { useState } from "react";
import { useTheme } from "next-themes";
import {
  BrainCircuit,
  Search,
  Plus,
  FileText,
  MessageSquare,
  ChartNoAxesCombined,
  Moon,
  Sun,
  Settings,
  ChevronDown,
  PanelLeftClose,
  PanelRightClose,
  Send,
  Sparkles,
  MoreHorizontal,
  BookOpen,
  Table2,
  Clock,
  Check,
} from "lucide-react";

const documents = [
  {
    id: 1,
    name: "Kotlin Programming Language.pdf",
    type: "PDF",
    pages: 245,
    color: "text-blue-500",
  },
  {
    id: 2,
    name: "Introduction to AR and VR.pdf",
    type: "PDF",
    pages: 128,
    color: "text-violet-500",
  },
  {
    id: 3,
    name: "Machine Learning Fundamentals.pdf",
    type: "PDF",
    pages: 86,
    color: "text-emerald-500",
  },
];

export default function Home() {
  const { theme, setTheme } = useTheme();

  const [selectedDocs, setSelectedDocs] = useState<number[]>([1, 2]);
  const [search, setSearch] = useState("");
  const [question, setQuestion] = useState("");

  const [sourcesOpen, setSourcesOpen] = useState(true);
  const [studioOpen, setStudioOpen] = useState(true);

  const filteredDocuments = documents.filter((doc) =>
    doc.name.toLowerCase().includes(search.toLowerCase())
  );

  function toggleDocument(id: number) {
    setSelectedDocs((current) =>
      current.includes(id)
        ? current.filter((item) => item !== id)
        : [...current, id]
    );
  }

  return (
    <div className="flex h-screen flex-col overflow-hidden bg-background text-foreground">

      {/* TOP NAVIGATION */}
      <header className="flex h-16 shrink-0 items-center justify-between border-b border-border bg-surface px-5">

        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary text-white">
            <BrainCircuit size={21} />
          </div>

          <div>
            <h1 className="text-sm font-bold tracking-tight">
              Document Intelligence
            </h1>
            <p className="text-xs text-muted">
              AI-powered research workspace
            </p>
          </div>
        </div>

        <div className="hidden items-center gap-2 sm:flex">
          <span className="rounded-lg border border-border bg-surface-secondary px-3 py-2 text-xs text-muted">
            My Workspace
          </span>

          <button
            onClick={() =>
              setTheme(theme === "dark" ? "light" : "dark")
            }
            className="rounded-lg border border-border p-2 transition hover:bg-surface-secondary"
            aria-label="Toggle theme"
          >
            {theme === "dark" ? (
              <Sun size={18} />
            ) : (
              <Moon size={18} />
            )}
          </button>

          <button
            className="rounded-lg p-2 text-muted transition hover:bg-surface-secondary hover:text-foreground"
            aria-label="Settings"
          >
            <Settings size={18} />
          </button>

          <div className="ml-2 flex h-8 w-8 items-center justify-center rounded-full bg-accent text-xs font-bold text-primary">
            D
          </div>
        </div>

        <button
          onClick={() =>
            setTheme(theme === "dark" ? "light" : "dark")
          }
          className="rounded-lg border border-border p-2 sm:hidden"
          aria-label="Toggle theme"
        >
          {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
        </button>
      </header>

      {/* MAIN WORKSPACE */}
      <main className="flex min-h-0 flex-1">

        {/* LEFT: SOURCES */}
        {sourcesOpen && (
          <aside className="hidden w-[280px] shrink-0 flex-col border-r border-border bg-surface md:flex">

            <div className="flex h-14 items-center justify-between border-b border-border px-4">
              <div className="flex items-center gap-2">
                <BookOpen size={17} />
                <h2 className="text-sm font-semibold">Sources</h2>
                <span className="rounded-md bg-surface-secondary px-2 py-0.5 text-xs text-muted">
                  {documents.length}
                </span>
              </div>

              <button
                onClick={() => setSourcesOpen(false)}
                className="rounded-md p-1.5 text-muted hover:bg-surface-secondary"
                aria-label="Hide sources"
              >
                <PanelLeftClose size={17} />
              </button>
            </div>

            <div className="p-4">
              <button className="flex w-full items-center justify-center gap-2 rounded-lg bg-primary px-3 py-2.5 text-sm font-medium text-white transition hover:opacity-90">
                <Plus size={17} />
                Add sources
              </button>

              <div className="relative mt-4">
                <Search
                  size={16}
                  className="absolute left-3 top-1/2 -translate-y-1/2 text-muted"
                />
                <input
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder="Search documents..."
                  className="w-full rounded-lg border border-border bg-background py-2 pl-9 pr-3 text-xs outline-none focus:border-primary"
                />
              </div>
            </div>

            <div className="flex items-center justify-between px-4 pb-2">
              <span className="text-xs font-medium text-muted">
                YOUR DOCUMENTS
              </span>

              <button className="text-xs text-primary">
                Select all
              </button>
            </div>

            <div className="flex-1 overflow-y-auto px-2">
              {filteredDocuments.map((doc) => {
                const selected = selectedDocs.includes(doc.id);

                return (
                  <button
                    key={doc.id}
                    onClick={() => toggleDocument(doc.id)}
                    className={`mb-1 flex w-full items-start gap-3 rounded-lg p-3 text-left transition ${
                      selected
                        ? "bg-accent"
                        : "hover:bg-surface-secondary"
                    }`}
                  >
                    <div
                      className={`mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-surface ${doc.color}`}
                    >
                      <FileText size={19} />
                    </div>

                    <div className="min-w-0 flex-1">
                      <p className="break-words text-xs font-medium leading-5">
                        {doc.name}
                      </p>
                      <p className="mt-1 text-xs text-muted">
                        {doc.pages} pages · {doc.type}
                      </p>
                    </div>

                    <div
                      className={`mt-1 flex h-4 w-4 shrink-0 items-center justify-center rounded border ${
                        selected
                          ? "border-primary bg-primary text-white"
                          : "border-border"
                      }`}
                    >
                      {selected && <Check size={11} />}
                    </div>
                  </button>
                );
              })}

              {filteredDocuments.length === 0 && (
                <p className="p-4 text-center text-xs text-muted">
                  No documents found.
                </p>
              )}
            </div>

            <div className="border-t border-border p-4">
              <p className="text-xs text-muted">
                {selectedDocs.length} documents selected
              </p>
            </div>
          </aside>
        )}

        {/* CENTER: CHAT */}
        <section className="flex min-w-0 flex-1 flex-col bg-background">

          <div className="flex h-14 shrink-0 items-center justify-between border-b border-border px-5">

            <div className="flex items-center gap-2">
              {!sourcesOpen && (
                <button
                  onClick={() => setSourcesOpen(true)}
                  className="rounded-md p-2 hover:bg-surface-secondary"
                  aria-label="Show sources"
                >
                  <BookOpen size={17} />
                </button>
              )}

              <MessageSquare size={17} />
              <h2 className="text-sm font-semibold">
                Research Assistant
              </h2>
            </div>

            <div className="flex items-center gap-2">
              <span className="hidden text-xs text-muted sm:block">
                {selectedDocs.length} sources active
              </span>

              {!studioOpen && (
                <button
                  onClick={() => setStudioOpen(true)}
                  className="rounded-md p-2 hover:bg-surface-secondary"
                  aria-label="Show studio"
                >
                  <ChartNoAxesCombined size={17} />
                </button>
              )}
            </div>
          </div>

          <div className="flex flex-1 flex-col items-center justify-center overflow-y-auto p-6">

            <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-accent text-primary">
              <Sparkles size={30} />
            </div>

            <h2 className="text-center text-2xl font-semibold tracking-tight">
              Your documents, understood.
            </h2>

            <p className="mt-3 max-w-md text-center text-sm leading-6 text-muted">
              Ask questions, discover insights, compare documents
              and explore your knowledge with AI.
            </p>

            <div className="mt-8 grid w-full max-w-lg gap-3 sm:grid-cols-2">

              {[
                "Summarize the selected documents",
                "Compare the key concepts",
                "Find important information",
                "Explain complex topics simply",
              ].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => setQuestion(suggestion)}
                  className="rounded-xl border border-border bg-surface p-4 text-left text-xs leading-5 transition hover:border-primary hover:bg-accent"
                >
                  <Sparkles
                    size={15}
                    className="mb-2 text-primary"
                  />
                  {suggestion}
                </button>
              ))}

            </div>
          </div>

          <div className="mx-auto w-full max-w-3xl px-5 pb-5">

            <div className="rounded-2xl border border-border bg-surface p-3 shadow-sm focus-within:border-primary">

              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask anything about your selected documents..."
                rows={2}
                className="w-full resize-none bg-transparent px-2 py-2 text-sm outline-none placeholder:text-muted"
              />

              <div className="flex items-center justify-between">
                <span className="text-xs text-muted">
                  {selectedDocs.length} sources selected
                </span>

                <button
                  onClick={() => setQuestion("")}
                  disabled={!question.trim()}
                  className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-xs font-medium text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  Ask AI
                  <Send size={14} />
                </button>
              </div>
            </div>

            <p className="mt-2 text-center text-xs text-muted">
              AI responses will include references to your source documents.
            </p>
          </div>
        </section>

        {/* RIGHT: STUDIO */}
        {studioOpen && (
          <aside className="hidden w-[290px] shrink-0 flex-col border-l border-border bg-surface lg:flex">

            <div className="flex h-14 items-center justify-between border-b border-border px-4">
              <div className="flex items-center gap-2">
                <ChartNoAxesCombined size={17} />
                <h2 className="text-sm font-semibold">Studio</h2>
              </div>

              <button
                onClick={() => setStudioOpen(false)}
                className="rounded-md p-1.5 text-muted hover:bg-surface-secondary"
                aria-label="Hide studio"
              >
                <PanelRightClose size={17} />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4">

              <p className="mb-4 text-xs leading-5 text-muted">
                Transform your documents into useful knowledge and insights.
              </p>

              <p className="mb-3 text-xs font-semibold text-muted">
                CREATE
              </p>

              {[
                {
                  icon: FileText,
                  title: "Document summary",
                  description: "Generate key takeaways",
                },
                {
                  icon: Table2,
                  title: "Data tables",
                  description: "Extract structured information",
                },
                {
                  icon: ChartNoAxesCombined,
                  title: "Charts and graphs",
                  description: "Visualize document data",
                },
                {
                  icon: MessageSquare,
                  title: "Document comparison",
                  description: "Compare multiple sources",
                },
              ].map((item) => {
                const Icon = item.icon;

                return (
                  <button
                    key={item.title}
                    className="mb-2 flex w-full items-center gap-3 rounded-xl border border-border p-3 text-left transition hover:bg-surface-secondary"
                  >
                    <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-accent text-primary">
                      <Icon size={18} />
                    </div>

                    <div className="min-w-0 flex-1">
                      <p className="text-xs font-semibold">
                        {item.title}
                      </p>
                      <p className="mt-1 text-xs text-muted">
                        {item.description}
                      </p>
                    </div>
                    <Plus size={15} className="text-muted" />
                  </button>
                );
              })}

              <div className="mb-3 mt-7 flex items-center justify-between">
                <p className="text-xs font-semibold text-muted">
                  RECENT ACTIVITY
                </p>
                <MoreHorizontal size={17} className="text-muted" />
              </div>

              <div className="rounded-xl border border-border p-3">
                <div className="flex items-center gap-2">
                  <FileText size={16} className="text-primary" />
                  <p className="text-xs font-medium">
                    Workspace ready
                  </p>
                </div>

                <div className="mt-2 flex items-center gap-2 text-xs text-muted">
                  <Clock size={12} />
                  Awaiting your first request
                </div>
              </div>

            </div>
          </aside>
        )}

      </main>
    </div>
  );
}
