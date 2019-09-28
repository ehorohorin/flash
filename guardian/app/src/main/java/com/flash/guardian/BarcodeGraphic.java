/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.flash.guardian;

import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.RectF;
import android.util.Log;

import com.flash.guardian.ui.camera.GraphicOverlay;
import com.google.android.gms.vision.barcode.Barcode;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.security.InvalidKeyException;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.KeyPairGeneratorSpi;
import java.security.NoSuchAlgorithmException;
import java.security.PublicKey;
import java.security.Signature;
import java.security.SignatureException;
import java.security.SignedObject;

/**
 * Graphic instance for rendering barcode position, size, and ID within an associated graphic
 * overlay view.
 */
public class BarcodeGraphic extends GraphicOverlay.Graphic {

    private static final String TAG = "BarcodeGraphic";
    private static final int COLOR_CHOICES[] = {
            Color.GREEN
    };
    private static int mCurrentColorIndex = 0;
    private int mId;
    private Paint mRectPaint;
    private Paint mTextPaint;
    private volatile Barcode mBarcode;

    private JSONObject jsonobj;
    private KeyPair keyPair;

    BarcodeGraphic(GraphicOverlay overlay) {
        super(overlay);

        mCurrentColorIndex = (mCurrentColorIndex + 1) % COLOR_CHOICES.length;
        final int selectedColor = COLOR_CHOICES[mCurrentColorIndex];

        mRectPaint = new Paint();
        mRectPaint.setColor(selectedColor);
        mRectPaint.setStyle(Paint.Style.STROKE);
        mRectPaint.setStrokeWidth(4.0f);

        mTextPaint = new Paint();
        mTextPaint.setColor(selectedColor);
        mTextPaint.setTextSize(36.0f);
    }

    public int getId() {
        return mId;
    }

    public void setId(int id) {
        this.mId = id;
    }

    public Barcode getBarcode() {
        return mBarcode;
    }

//    http://java-online.ru/blog-signature.xhtml
    private boolean verifySignedObject(final SignedObject obj, PublicKey key)
            throws InvalidKeyException, SignatureException,
            NoSuchAlgorithmException
    {
        // Verify the signed object
        Signature signature = Signature.getInstance(key.getAlgorithm());
        return obj.verify(key, signature);
    }

    /**
     * Updates the barcode instance from the detection of the most recent frame.  Invalidates the
     * relevant portions of the overlay to trigger a redraw.
     */
    void updateItem(Barcode barcode) {
        mBarcode = barcode;
        postInvalidate();
    }

    /**
     * Draws the barcode annotations for position, size, and raw value on the supplied canvas.
     */
    @Override
    public void draw(Canvas canvas) {
        Barcode barcode = mBarcode;
        if (barcode == null) {
            return;
        }

        // Draws the bounding box around the barcode.
        RectF rect = new RectF(barcode.getBoundingBox());
        rect.left = translateX(rect.left);
        rect.top = translateY(rect.top);
        rect.right = translateX(rect.right);
        rect.bottom = translateY(rect.bottom);
        canvas.drawRect(rect, mRectPaint);

        Log.d("Barcode scaned", barcode.rawValue);
        String name = "";

        //TODO инициализировать
        SignedObject signedObject = null;
//        PublicKey publicKey  = (PublicKey) readKey(FILE_public);
        PublicKey publicKey  = null;


        try {
            jsonobj = new JSONObject(barcode.rawValue);
            name = jsonobj.getString("name");
            Log.d(TAG, jsonobj.getString("name"));
            Signature signature = Signature.getInstance("SHA256WithDSA");

            signature.initVerify(keyPair.getPublic());



            // Проверка подписанного объекта

            boolean verified = verifySignedObject(signedObject, publicKey);
            Log.d(TAG, "Проверка подписи объекта : " + verified);

            // Извлечение подписанного объекта
            String unsignedObject = (String) signedObject.getObject();

            Log.d(TAG, "Исходный текст объекта : " + unsignedObject);
            KeyPairGeneratorSpi keyPairGenerator = null;
            KeyPair keyPair = keyPairGenerator.generateKeyPair();

            public class PrintablePGPPublicKey  {
                PGPPublicKey base;

                public PrintablePGPPublicKey(PGPPublicKey iBase){
                    base = iBase;
                }

                public PGPPublicKey getPublicKey(){
                    return base;
                }

                @Override
                public String toString() {
                    StringBuilder outStr = new StringBuilder();
                    Iterator iter = base.getUserIDs();

                    outStr.append("[0x");
                    outStr.append(Integer.toHexString((int)base.getKeyID()).toUpperCase());
                    outStr.append("] ");

                    while(iter.hasNext()){
                        outStr.append(iter.next().toString());
                        outStr.append("; ");
                    }

                    return outStr.toString();
                }

                class PGPPublicKey {
                }
            }

        } catch (JSONException e) {
            e.printStackTrace();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (InvalidKeyException e) {
            e.printStackTrace();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (SignatureException e) {
            e.printStackTrace();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }


        // Draws a label at the bottom of the barcode indicate the barcode value that was detected.
//        canvas.drawText(barcode.rawValue, rect.left, rect.bottom, mTextPaint);
        canvas.drawText(name, rect.left, rect.bottom, mTextPaint);

    }

    private Object readKey(final String filePath)
            throws FileNotFoundException,
            IOException, ClassNotFoundException
    {
        FileInputStream fis = new FileInputStream(filePath);
        ObjectInputStream ois = new ObjectInputStream(fis);
        Object object = ois.readObject();
        return object;
    }
}
