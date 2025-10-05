import React, { useState, useEffect } from 'react';

export function DragIndicator() {
    // 6 dots indicating that the icons are draggable
    const num_dots = 6;

    const dot = (i) => (
        <div
            className='rounded-full bg-gray-200 lg:size-1 md:size-[3px] sm:size-[2px] inset-shadow-sm'
            key={i}
        />
    );

    return (
        <div
            className='w-3 flex flex-row flex-wrap gap-[2px] ml-1'
        >
            {[...Array(num_dots)].map((_, i) => 
                dot(i)
            )}
        </div>
    );
};



export default function PlayerIcon(props) {
    // Player icon given an id, name, and team's color
    const data = {
        primaryColor: props?.primaryColor || '#FFFFFF',
        secondaryColor: props?.secondaryColor || '000000',
        name: props?.name || 'test', 
        lastName: props?.lastName || 'test'
    }
    console.log(props?.src)

    return (
    
        <div 
            className='lg:size-30 md:size-20 sm:size-17 border-white border-2 rounded-xl shadow-lg/35 flex flex-row items-center
                        transition-all ease-in-out duration-100'
            style={{backgroundColor: props.primaryColor}}
        >
            <DragIndicator />
            <div
                className='flex flex-col items-center justify-start gap-y-0'
                style={{backgroundColor: props.primaryColor}}
            >
                <img 
                    src={props?.src || 'qb-faces/default.png'}
                    onError={(e) => { e.target.src = 'qb-faces/default.png'; }}
                    width={80}
                    height={80}
                    className="block my-1 lg:w-20 lg:h-20 md:w-15 md:h-12 sm:w-12 sm:h-10 sm:mb-[-2px] md:mb-1 lg:mb-1"
                    alt="face pixel art"
                    draggable={false}
                />
                <div
                    className='bg-white/85 font-semibold rounded-md px-1 text-black lg:text-base md:text-sm sm:text-xs'
                >
                    {data.lastName}
                </div>
            </div>
            <DragIndicator />
        </div>
    )
}
