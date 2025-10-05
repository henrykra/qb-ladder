import PlayerIcon from './PlayerIcon';

function PlaceHolder() {
    return (
        <div className='invisible'>
            <PlayerIcon name='Williams' />
        </div>
    );
}

export default function Container({ draggables, ranks, activeId }) {
    // Element containing player icons before ranking. 
    // As icons are placed on the ladder, placeholders are put in the container.
    return (
       <div className='absolute bottom-0 lg:h-40 lg:w-150
                          bg-gray-200 dark:bg-gray-400/80 
                          lg:p-4 md:p-3 sm:p-1 lg:m-4 sm:m-3 flex flex-row flex-wrap border-2 
                          rounded-xl shadow-md/30 gap-2 items-center justify-evenly'
          >
            {
              draggables.map((element, index) => {
                if (ranks.includes(element.props.id) || activeId === element.props.id) {
                  return <PlaceHolder key={index} />;
                } else {
                  return element;
                }
              })
            }
        </div>
    );
}