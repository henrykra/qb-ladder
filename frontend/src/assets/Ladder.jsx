import Droppable from './Droppable';

export default function Ladder({ ranks, draggables, locked, loading, handleReset }) {
    // Ladder element holding droppable areas. 
    return (
        <div 
            className="lg:h-180 lg:w-70 md:h-125 md:w-45 sm:w-35 sm:h-100 flex flex-col 
                        items-center justify-center gap-4 bg-[url(/ladder.png)]
                        bg-size-[100%_100%] transition-all ease-in-out duration-100" 
        >
            {
            ranks.map((itemId, rankIndex) => {
                return (
                <Droppable id={rankIndex} key={rankIndex} full={itemId} locked={locked}>
                    {itemId ? draggables[itemId] : <div>{`Rank ${rankIndex + 1}`}</div>}
                </Droppable>
                );
            })
            }
            <button 
            className={`absolute bg-slate-200 dark:bg-gray-800/80 bottom-2.5 border-2 lg:p-3 md:p-2 sm:p-1 rounded-xl
                shadow-md/30 hover:shadow-md/15 transition-all duration-200 
            hover:border-sky-400 active:border-white 
                transition-all duration-200 lg:text-base md:text-sm sm:text-xs
                ${locked & !loading ? "opacity-100 cursor-pointer": "opacity-0"}`}
            onClick={handleReset}
            disabled={!locked | loading}
            >
            <strong>Reset</strong>
            </button>

        </div>
    );
}