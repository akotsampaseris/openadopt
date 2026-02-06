import { useState } from "react";
import { useDropzone } from "react-dropzone";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuth } from "../../context/AuthContext";
import toast from "react-hot-toast";
import Lightbox from "yet-another-react-lightbox";
import Video from "yet-another-react-lightbox/plugins/video";
import Thumbnails from "yet-another-react-lightbox/plugins/thumbnails";
import "yet-another-react-lightbox/styles.css";
import "yet-another-react-lightbox/plugins/thumbnails.css";
import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation, Pagination } from "swiper/modules";
import "swiper/swiper-bundle.css";

import {
    uploadAnimalPrimaryPhoto,
    uploadAnimalFile,
    deleteAnimalFile,
} from "../../api/animals";
import ConfirmModal from "../ui/ConfirmModal";

interface PhotoUploadProps {
    animalId: number;
    primaryPhotoUrl?: string;
    extraPhotosUrl?: string;
}

export default function AnimalPhotoManagement({
    animalId,
    primaryPhotoUrl,
    extraPhotosUrl,
}: PhotoUploadProps) {
    const { accessToken } = useAuth();
    const queryClient = useQueryClient();
    const [lightboxOpen, setLightboxOpen] = useState(false);
    const [lightboxIndex, setLightboxIndex] = useState(0);
    const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);

    const extraPhotos = (() => {
        try {
            return extraPhotosUrl ? JSON.parse(extraPhotosUrl) : [];
        } catch {
            return [];
        }
    })();

    const allPhotos = [
        ...(primaryPhotoUrl ? [{ type: "image", src: primaryPhotoUrl }] : []),
        ...extraPhotos.map((url: string) => {
            const properties: any = {};
            if (url.match(/\.(mp4|mpeg|mov|quicktime)$/i)) {
                properties["type"] = "video";
                properties["sources"] = [
                    {
                        src: url,
                        type: "video/mp4",
                    },
                ];
            } else {
                properties["type"] = "image";
                properties["src"] = url;
            }
            return properties;
        }),
    ];

    // Primary photo upload
    const uploadPrimaryMutation = useMutation({
        mutationFn: async (file: File) =>
            uploadAnimalPrimaryPhoto(accessToken!, animalId, file),
        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["animal", String(animalId)],
            });
            toast.success("Primary photo uploaded successfully!");
        },
        onError: (error: any) => {
            const message = error.response?.data?.detail || "Upload failed";
            toast.error(message);
        },
    });

    // Extra photo upload
    const uploadExtraMutation = useMutation({
        mutationFn: async (file: File) =>
            uploadAnimalFile(accessToken!, animalId, file),
        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["animal", String(animalId)],
            });
            toast.success("File added successfully!");
        },
        onError: (error: any) => {
            const message = error.response?.data?.detail || "Upload failed";
            toast.error(message);
        },
    });

    // Delete extra photo
    const deleteExtraMutation = useMutation({
        mutationFn: async (url: string) =>
            deleteAnimalFile(accessToken!, animalId, url),
        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["animal", String(animalId)],
            });
            toast.success("Photo deleted successfully!");
        },
        onError: () => {
            toast.error("Failed to delete photo");
        },
    });

    // Primary photo dropzone
    const primaryDropzone = useDropzone({
        accept: { "image/*": [".jpg", ".jpeg", ".png", ".gif", ".webp"] },
        maxSize: 5 * 1024 * 1024, // 5MB
        maxFiles: 1,
        onDrop: (acceptedFiles, rejectedFiles) => {
            if (rejectedFiles.length > 0) {
                const error = rejectedFiles[0].errors[0];
                if (error.code === "file-too-large") {
                    toast.error("File too large. Maximum size is 5MB");
                } else if (error.code === "file-invalid-type") {
                    toast.error("Invalid file type. Only images allowed");
                }
                return;
            }

            if (acceptedFiles.length > 0) {
                uploadPrimaryMutation.mutate(acceptedFiles[0]);
            }
        },
    });

    // Extra photos dropzone
    const extraDropzone = useDropzone({
        accept: {
            "image/*": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
            "video/*": [".mp4", ".mpeg", ".quicktime", ".mov"],
        },
        maxSize: 6 * 1024 * 1024,
        maxFiles: 10,
        onDrop: (acceptedFiles, rejectedFiles) => {
            if (rejectedFiles.length > 0) {
                const error = rejectedFiles[0].errors[0];
                if (error.code === "file-too-large") {
                    toast.error("File too large. Maximum size is 5MB");
                } else if (error.code === "file-invalid-type") {
                    toast.error(
                        "Invalid file type. Only images and videos allowed",
                    );
                }
                return;
            }

            if (extraPhotos.length >= 10) {
                toast.error("Maximum 10 extra photos/videos allowed");
                return;
            }

            if (acceptedFiles.length > 0) {
                uploadExtraMutation.mutate(acceptedFiles[0]);
            }
        },
    });

    const handleDeletePhoto = (url: string) => {
        setDeleteConfirm(url);
    };

    const confirmDelete = () => {
        if (deleteConfirm) {
            deleteExtraMutation.mutate(deleteConfirm);
            setDeleteConfirm(null);
        }
    };

    const openLightbox = (index: number) => {
        setLightboxIndex(index);
        setLightboxOpen(true);
    };

    return (
        <>
            <div className="rounded-lg p-6">
                <h2 className="text-xl font-bold mb-4">Photos & Videos</h2>
                {/* Primary Photo */}
                <div className="mb-8">
                    <h3 className="font-semibold mb-3 flex items-center justify-between">
                        <span>Primary Photo</span>
                        <span className="text-xs text-gray-500">
                            Max 5MB • JPG, PNG, GIF, WebP
                        </span>
                    </h3>

                    {primaryPhotoUrl ? (
                        <div className="relative group">
                            <img
                                src={primaryPhotoUrl}
                                alt="Primary"
                                className="w-full h-80 object-cover rounded-lg cursor-pointer transition-opacity group-hover:opacity-90"
                                onClick={() => openLightbox(0)}
                            />
                            <div
                                {...primaryDropzone.getRootProps()}
                                className="absolute inset-0 bg-black bg-opacity-50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center rounded-lg cursor-pointer"
                            >
                                <input {...primaryDropzone.getInputProps()} />
                                <p className="text-white font-semibold">
                                    {uploadPrimaryMutation.isPending
                                        ? "Uploading..."
                                        : "Click or drop to replace"}
                                </p>
                            </div>
                        </div>
                    ) : (
                        <div
                            {...primaryDropzone.getRootProps()}
                            className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
                                primaryDropzone.isDragActive
                                    ? "border-blue-500 bg-blue-50"
                                    : "border-gray-300 hover:border-gray-400"
                            }`}
                        >
                            <input {...primaryDropzone.getInputProps()} />
                            <div className="text-gray-600">
                                {uploadPrimaryMutation.isPending ? (
                                    <p className="text-blue-600 font-semibold">
                                        Uploading...
                                    </p>
                                ) : primaryDropzone.isDragActive ? (
                                    <p className="text-blue-600">
                                        Drop the image here
                                    </p>
                                ) : (
                                    <>
                                        <p className="font-semibold mb-1">
                                            Drag & drop an image here
                                        </p>
                                        <p className="text-sm">
                                            or click to select
                                        </p>
                                    </>
                                )}
                            </div>
                        </div>
                    )}
                </div>
                Extra Photos/Videos
                <div>
                    <h3 className="font-semibold mb-3 flex items-center justify-between">
                        <span>Files uploaded ({extraPhotos.length}/10)</span>
                        <span className="text-xs text-gray-500">
                            Max 5MB each • JPG, PNG, GIF, WebP • MP4, MPEG,
                            Quicktime, MOV
                        </span>
                    </h3>

                    {extraPhotos.length > 0 && (
                        <div className="mb-4">
                            <Swiper
                                modules={[Navigation, Pagination]}
                                spaceBetween={16}
                                slidesPerView={1}
                                navigation
                                pagination={{ clickable: true }}
                                breakpoints={{
                                    640: { slidesPerView: 2 },
                                    768: { slidesPerView: 3 },
                                    1024: { slidesPerView: 4 },
                                }}
                                className="mb-4"
                            >
                                {extraPhotos.map(
                                    (url: string, index: number) => {
                                        const isVideo = url.match(
                                            /\.(mp4|mpeg|mov|quicktime)$/i,
                                        );
                                        return (
                                            <SwiperSlide key={url}>
                                                <div className="relative group">
                                                    {isVideo ? (
                                                        <video
                                                            src={url}
                                                            className="w-full h-40 object-cover rounded-lg cursor-pointer"
                                                            onClick={() =>
                                                                openLightbox(
                                                                    primaryPhotoUrl
                                                                        ? index +
                                                                              1
                                                                        : index,
                                                                )
                                                            }
                                                            muted
                                                            loop
                                                            onMouseEnter={(e) =>
                                                                e.currentTarget.play()
                                                            }
                                                            onMouseLeave={(
                                                                e,
                                                            ) => {
                                                                e.currentTarget.pause();
                                                                e.currentTarget.currentTime = 0;
                                                            }}
                                                        />
                                                    ) : (
                                                        <img
                                                            src={url}
                                                            alt={`Extra ${index + 1}`}
                                                            className="w-full h-40 object-cover rounded-lg cursor-pointer transition-transform group-hover:scale-105"
                                                            onClick={() =>
                                                                openLightbox(
                                                                    primaryPhotoUrl
                                                                        ? index +
                                                                              1
                                                                        : index,
                                                                )
                                                            }
                                                        />
                                                    )}
                                                    <button
                                                        onClick={(e) => {
                                                            e.stopPropagation();
                                                            handleDeletePhoto(
                                                                url,
                                                            );
                                                        }}
                                                        disabled={
                                                            deleteExtraMutation.isPending
                                                        }
                                                        className="absolute top-2 right-2 bg-red-600 text-white rounded-full w-8 h-8 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-700 disabled:bg-gray-400"
                                                        title="Delete photo"
                                                    >
                                                        ×
                                                    </button>
                                                </div>
                                            </SwiperSlide>
                                        );
                                    },
                                )}
                            </Swiper>
                        </div>
                    )}

                    {extraPhotos.length < 10 && (
                        <div
                            {...extraDropzone.getRootProps()}
                            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                                extraDropzone.isDragActive
                                    ? "border-blue-500 bg-blue-50"
                                    : "border-gray-300 hover:border-gray-400"
                            }`}
                        >
                            <input {...extraDropzone.getInputProps()} />
                            <div className="text-gray-600">
                                {uploadExtraMutation.isPending ? (
                                    <p className="text-blue-600 font-semibold">
                                        Uploading...
                                    </p>
                                ) : extraDropzone.isDragActive ? (
                                    <p className="text-blue-600">
                                        Drop the image here
                                    </p>
                                ) : (
                                    <>
                                        <p className="font-semibold mb-1">
                                            + Add Photo
                                        </p>
                                        <p className="text-sm">
                                            Drag & drop or click to select
                                        </p>
                                    </>
                                )}
                            </div>
                        </div>
                    )}
                </div>
                {/* Lightbox */}
                <Lightbox
                    open={lightboxOpen}
                    close={() => setLightboxOpen(false)}
                    index={lightboxIndex}
                    slides={allPhotos}
                    plugins={[Video, Thumbnails]}
                />
            </div>
            <ConfirmModal
                isOpen={deleteConfirm !== null}
                title="Delete Photo"
                message="Are you sure you want to delete this photo? This action cannot be undone."
                confirmText="Delete"
                cancelText="Cancel"
                onConfirm={confirmDelete}
                onCancel={() => setDeleteConfirm(null)}
                isDangerous
            />
        </>
    );
}
