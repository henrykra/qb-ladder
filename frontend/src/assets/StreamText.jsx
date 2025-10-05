import React, { useState, useEffect, useRef } from 'react';

export default function StreamText({enabled, locked, setLocked, loading, setLoading, ranks, draggables}) {
    const [text, setText] = useState("");
    const boxRef = useRef(null);

    useEffect(() => {
        if (boxRef.current) {
            boxRef.current.scrollTop = boxRef.current.scrollHeight;
        }
    }, [text]); // update scroll every time text changes

    const handleClick = async () => {
        setText("\t\t");
        setLoading(true);
        setLocked(true);

        const ranking = ranks.map((element, index) => {
            return draggables[element].props.pid;
        })
        console.log(ranking)

        try {
            const response = await fetch("/api/stream/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ qb_list: ranking}),
            });
            
            if (!response.body) {
                throw new Error("ReadibleStream not supported");
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder("utf-8");

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                setText((prev) => prev + chunk)
            }

        } catch (err) {
            console.error("Stream error: ", err);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className={`mt-4 mx-8 w-100% whitespace-pre-wrap border-2
                        rounded-xl shadow-md/30 bg-gray-50 dark:bg-gray-800/80
                        ${locked ? "max-h-[90%]" : "max-h-0%"}
                        transition-all duration-300
                        overflow-y-auto flex flex-col
                            ${enabled ? "" : "opacity-30"} transition-all duration-200`}
            ref={boxRef}>
            <div className="sticky top-0 bg-gray-50/90 dark:bg-gray-400/80 py-1 shadow-sm/5 rounded-lg">
                <button
                    onClick={handleClick}
                    disabled={loading | !enabled}
                    className={`w-20 lg:h-20 lg:w-20 md:h-12 md:w-18
                    my-2 mx-4 border-2 border-white bg-sky-500/70
                    rounded-full shadow-md/30
                    transition-all duration-200 ease-in-out
                    sticky top-0 flex-shrink-0 inline
                    ${enabled ? "hover:shadow-md/15 cursor-pointer" : ""}`}
                > {loading ? "..." : "Press"} </button>
                <div
                    className="inline-block pr-4 md:text-base sm:text-sm">
                    {enabled ? "Argue your ranking!" : "Fill out your ranking!"}
                </div>
            </div>
            <div className={`${enabled && locked ? 'p-2' : 'p-0'} sm:text-sm md:text-base`}>
                {enabled && locked ? text : ""}
            </div>
        </div>
    );
}