        I = imread('sample_images/blocks_bk_src.tif');
        %tform = affine2d([1 0 0; .5 1 0; 0 0 1]);
        %outputView = imref2d(size(template));
        %J = imwarp(I,tform,'OutputView',outputView);
       % J = imwarp(I,tform);
        imshow(I)
%        figure, montage({I, J});
st = regionprops(BW, 'BoundingBox' );
 rectangle('Position',[st.BoundingBox(1),st.BoundingBox(2),st.BoundingBox(3),st.BoundingBox(4)],...
'EdgeColor','r','LineWidth',2 )